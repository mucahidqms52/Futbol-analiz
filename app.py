from flask import Flask, render_template, request
from scipy.stats import poisson
import numpy as np

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        try:
            # 1. Kullanıcıdan gelen verileri al
            league_home_avg = float(request.form['league_home_avg'])
            league_away_avg = float(request.form['league_away_avg'])
            
            home_scored = float(request.form['home_scored'])
            home_conceded = float(request.form['home_conceded'])
            away_scored = float(request.form['away_scored'])
            away_conceded = float(request.form['away_conceded'])
            
            # Kullanıcının girdiği oranlar (Value bulmak için)
            market_1 = float(request.form['market_1'])
            market_2_5_ust = float(request.form['market_2_5_ust'])
            market_kg_var = float(request.form['market_kg_var'])

            # 2. Güç Hesaplamaları (Güç Endeksleri)
            home_attack = home_scored / league_home_avg
            home_defense = home_conceded / league_away_avg
            away_attack = away_scored / league_away_avg
            away_defense = away_conceded / league_home_avg

            # 3. Beklenen Goller (xG - Lambda)
            home_xg = home_attack * away_defense * league_home_avg
            away_xg = away_attack * home_defense * league_away_avg

            # 4. Poisson Dağılımı ile Skor Matrisi (0'dan 6 gole kadar)
            max_goals = 6
            home_probs = [poisson.pmf(i, home_xg) for i in range(max_goals + 1)]
            away_probs = [poisson.pmf(i, away_xg) for i in range(max_goals + 1)]

            # Olasılık Matrisi
            score_matrix = np.outer(home_probs, away_probs)

            # 5. Olasılıkları Toplama
            prob_1 = sum(score_matrix[i, j] for i in range(max_goals + 1) for j in range(max_goals + 1) if i > j)
            prob_X = sum(score_matrix[i, j] for i in range(max_goals + 1) for j in range(max_goals + 1) if i == j)
            prob_2 = sum(score_matrix[i, j] for i in range(max_goals + 1) for j in range(max_goals + 1) if i < j)
            
            prob_over_2_5 = sum(score_matrix[i, j] for i in range(max_goals + 1) for j in range(max_goals + 1) if (i + j) > 2.5)
            prob_kg_var = sum(score_matrix[i, j] for i in range(max_goals + 1) for j in range(max_goals + 1) if i > 0 and j > 0)

            # Kombinasyonlar (Örn: 1 ve 2.5 Üst = Ev kazanır ve toplam gol 2.5 üstü)
            prob_1_ve_ust = sum(score_matrix[i, j] for i in range(max_goals + 1) for j in range(max_goals + 1) if i > j and (i + j) > 2.5)
            prob_1_ve_kg = sum(score_matrix[i, j] for i in range(max_goals + 1) for j in range(max_goals + 1) if i > j and i > 0 and j > 0)

            # 6. Value (Değer) Hesaplamaları ( (Olasılık x Oran) - 1 )
            value_1 = (prob_1 * market_1) - 1
            value_2_5 = (prob_over_2_5 * market_2_5_ust) - 1
            value_kg = (prob_kg_var * market_kg_var) - 1

            # Sonuçları şablona gönder
            results = {
                'home_xg': round(home_xg, 2),
                'away_xg': round(away_xg, 2),
                'prob_1': round(prob_1 * 100, 1),
                'prob_X': round(prob_X * 100, 1),
                'prob_2': round(prob_2 * 100, 1),
                'prob_over_2_5': round(prob_over_2_5 * 100, 1),
                'prob_kg_var': round(prob_kg_var * 100, 1),
                'prob_1_ve_ust': round(prob_1_ve_ust * 100, 1),
                'prob_1_ve_kg': round(prob_1_ve_kg * 100, 1),
                'value_1': round(value_1 * 100, 1),
                'value_2_5': round(value_2_5 * 100, 1),
                'value_kg': round(value_kg * 100, 1),
                'fair_odd_1': round(1 / prob_1, 2) if prob_1 > 0 else 0,
                'fair_odd_ust': round(1 / prob_over_2_5, 2) if prob_over_2_5 > 0 else 0,
                'fair_odd_kg': round(1 / prob_kg_var, 2) if prob_kg_var > 0 else 0,
            }
            return render_template('index.html', results=results)
            
        except Exception as e:
            return render_template('index.html', error=f"Hata: {str(e)}")

    return render_template('index.html', results=None)

if __name__ == '__main__':
    app.run(debug=True)
