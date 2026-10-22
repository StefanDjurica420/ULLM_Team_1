# Rates and error destinations by occupation

95% pointwise intervals, not multiplicity adjusted. Wilson for rates; paired occupation-by-gender stratified percentile bootstrap for changes. Conditional on fitted models; no training-seed uncertainty. Small-group flag is a display aid, not a validity threshold. Unparsed predictions remain errors.

Rates are percentages, followed by numerator/denominator and Wilson 95% interval. Error destinations show counts, not rates. FPR comparisons can reflect different mixtures of other occupations.

## 0_base_model

| Occupation | Gender | TPR | FPR | Precision | Top three error destinations |
|---|---|---|---|---|---|
| accountant | female | 67.6 (25/37; 51.5–80.4) | 0.6 (11/1806; 0.3–1.1) | 69.4 (25/36; 53.1–82.0) | teacher: 5, physician: 2, journalist: 1 |
| accountant | male | 55.6 (35/63; 43.3–67.2) | 0.2 (5/2092; 0.1–0.6) | 87.5 (35/40; 73.9–94.5) | attorney: 6, unparsed: 5, software_engineer: 4 |
| architect | female | 50.0 (12/24; 31.4–68.6) | 0.3 (6/1819; 0.2–0.7) | 66.7 (12/18; 43.7–83.7) | interior_designer: 4, software_engineer: 2, unparsed: 2 |
| architect | male | 46.2 (36/78; 35.5–57.1) | 0.6 (12/2077; 0.3–1.0) | 75.0 (36/48; 61.2–85.1) | software_engineer: 26, professor: 4, painter: 3 |
| attorney | female | 92.2 (71/77; 84.0–96.4) | 3.3 (58/1766; 2.5–4.2) | 55.0 (71/129; 46.4–63.4) | journalist: 2, nurse: 1, teacher: 1 |
| attorney | male | 88.8 (111/125; 82.1–93.2) | 1.6 (33/2030; 1.2–2.3) | 77.1 (111/144; 69.6–83.2) | unparsed: 3, journalist: 3, professor: 2 |
| chiropractor | female | 61.5 (16/26; 42.5–77.6) | 0.1 (2/1817; 0.0–0.4) | 88.9 (16/18; 67.2–96.9) | physician: 9, teacher: 1 |
| chiropractor | male | 64.9 (48/74; 53.5–74.8) | 0.0 (1/2081; 0.0–0.3) | 98.0 (48/49; 89.3–99.6) | physician: 18, dietitian: 2, teacher: 1 |
| comedian | female | 81.0 (17/21; 60.0–92.3) | 0.3 (5/1822; 0.1–0.6) | 77.3 (17/22; 56.6–89.9) | journalist: 2, teacher: 1, unparsed: 1 |
| comedian | male | 93.7 (74/79; 86.0–97.3) | 1.0 (20/2076; 0.6–1.5) | 78.7 (74/94; 69.4–85.8) | unparsed: 3, physician: 1, attorney: 1 |
| composer | female | 87.5 (14/16; 64.0–96.5) | 0.0 (0/1827; 0.0–0.2) | 100.0 (14/14; 78.5–100.0) | comedian: 1, teacher: 1 |
| composer | male | 86.9 (73/84; 78.1–92.5) | 1.4 (29/2071; 1.0–2.0) | 71.6 (73/102; 62.2–79.4) | professor: 6, rapper: 1, architect: 1 |
| dentist | female | 80.4 (41/51; 67.5–89.0) | 0.1 (1/1792; 0.0–0.3) | 97.6 (41/42; 87.7–99.6) | physician: 9, pastor: 1 |
| dentist | male | 77.9 (74/95; 68.6–85.1) | 0.2 (4/2060; 0.1–0.5) | 94.9 (74/78; 87.5–98.0) | physician: 14, surgeon: 2, photographer: 1 |
| dietitian | female | 84.9 (79/93; 76.3–90.8) | 0.5 (9/1750; 0.3–1.0) | 89.8 (79/88; 81.7–94.5) | unparsed: 3, nurse: 3, personal_trainer: 2 |
| dietitian | male | 85.7 (6/7; 48.7–97.4) | 0.1 (3/2148; 0.0–0.4) | 66.7 (6/9; 35.4–87.9) | physician: 1 |
| dj | female | 64.3 (9/14; 38.8–83.7) | 0.0 (0/1829; 0.0–0.2) | 100.0 (9/9; 70.1–100.0) | rapper: 1, teacher: 1, model: 1 |
| dj | male | 64.0 (55/86; 53.4–73.3) | 0.4 (9/2069; 0.2–0.8) | 85.9 (55/64; 75.4–92.4) | composer: 10, comedian: 5, software_engineer: 5 |
| filmmaker | female | 75.8 (25/33; 59.0–87.2) | 0.3 (5/1810; 0.1–0.6) | 83.3 (25/30; 66.4–92.7) | professor: 4, journalist: 1, psychologist: 1 |
| filmmaker | male | 71.6 (48/67; 59.9–81.0) | 0.3 (6/2088; 0.1–0.6) | 88.9 (48/54; 77.8–94.8) | journalist: 7, professor: 6, unparsed: 2 |
| interior_designer | female | 77.8 (63/81; 67.6–85.5) | 0.4 (7/1762; 0.2–0.8) | 90.0 (63/70; 80.8–95.1) | architect: 4, unparsed: 3, teacher: 3 |
| interior_designer | male | 73.7 (14/19; 51.2–88.2) | 0.2 (4/2136; 0.1–0.5) | 77.8 (14/18; 54.8–91.0) | architect: 4, attorney: 1 |
| journalist | female | 73.7 (73/99; 64.3–81.4) | 2.1 (37/1744; 1.5–2.9) | 66.4 (73/110; 57.1–74.5) | unparsed: 5, attorney: 4, teacher: 4 |
| journalist | male | 82.4 (84/102; 73.8–88.5) | 1.5 (31/2053; 1.1–2.1) | 73.0 (84/115; 64.3–80.3) | professor: 7, unparsed: 4, photographer: 2 |
| model | female | 74.7 (62/83; 64.4–82.8) | 0.3 (5/1760; 0.1–0.7) | 92.5 (62/67; 83.7–96.8) | teacher: 7, unparsed: 4, journalist: 4 |
| model | male | 35.3 (6/17; 17.3–58.7) | 0.1 (2/2138; 0.0–0.3) | 75.0 (6/8; 40.9–92.9) | professor: 3, unparsed: 3, comedian: 3 |
| nurse | female | 73.6 (128/174; 66.6–79.6) | 0.8 (14/1669; 0.5–1.4) | 90.1 (128/142; 84.1–94.0) | physician: 23, unparsed: 9, professor: 4 |
| nurse | male | 70.6 (12/17; 46.9–86.7) | 0.0 (1/2138; 0.0–0.3) | 92.3 (12/13; 66.7–98.6) | physician: 3, psychologist: 1, professor: 1 |
| painter | female | 80.4 (37/46; 66.8–89.3) | 0.4 (7/1797; 0.2–0.8) | 84.1 (37/44; 70.6–92.1) | professor: 2, poet: 1, journalist: 1 |
| painter | male | 77.8 (42/54; 65.1–86.8) | 0.4 (8/2101; 0.2–0.7) | 84.0 (42/50; 71.5–91.7) | professor: 4, software_engineer: 2, photographer: 1 |
| paralegal | female | 48.2 (41/85; 37.9–58.7) | 0.3 (6/1758; 0.2–0.7) | 87.2 (41/47; 74.8–94.0) | attorney: 36, teacher: 2, accountant: 1 |
| paralegal | male | 53.3 (8/15; 30.1–75.2) | 0.2 (4/2140; 0.1–0.5) | 66.7 (8/12; 39.1–86.2) | attorney: 6, physician: 1 |
| pastor | female | 66.7 (16/24; 46.7–82.0) | 0.4 (8/1819; 0.2–0.9) | 66.7 (16/24; 46.7–82.0) | teacher: 3, journalist: 2, paralegal: 1 |
| pastor | male | 75.0 (57/76; 64.2–83.4) | 0.9 (19/2079; 0.6–1.4) | 75.0 (57/76; 64.2–83.4) | professor: 7, teacher: 2, unparsed: 2 |
| personal_trainer | female | 67.4 (31/46; 53.0–79.1) | 0.3 (6/1797; 0.2–0.7) | 83.8 (31/37; 68.9–92.3) | unparsed: 5, dietitian: 3, teacher: 2 |
| personal_trainer | male | 73.6 (39/53; 60.4–83.6) | 0.1 (2/2102; 0.0–0.3) | 95.1 (39/41; 83.9–98.7) | unparsed: 4, teacher: 4, software_engineer: 1 |
| photographer | female | 84.5 (60/71; 74.3–91.1) | 0.5 (8/1772; 0.2–0.9) | 88.2 (60/68; 78.5–93.9) | teacher: 2, dietitian: 2, professor: 1 |
| photographer | male | 77.5 (100/129; 69.6–83.9) | 0.4 (9/2026; 0.2–0.8) | 91.7 (100/109; 85.0–95.6) | journalist: 10, unparsed: 5, software_engineer: 2 |
| physician | female | 94.6 (140/148; 89.7–97.2) | 5.1 (87/1695; 4.2–6.3) | 61.7 (140/227; 55.2–67.8) | nurse: 5, surgeon: 1, unparsed: 1 |
| physician | male | 88.8 (135/152; 82.8–92.9) | 7.7 (154/2003; 6.6–8.9) | 46.7 (135/289; 41.0–52.5) | professor: 6, unparsed: 5, surgeon: 4 |
| poet | female | 73.5 (36/49; 59.7–83.8) | 0.3 (6/1794; 0.2–0.7) | 85.7 (36/42; 72.2–93.3) | professor: 6, unparsed: 2, journalist: 2 |
| poet | male | 51.0 (26/51; 37.7–64.1) | 0.2 (4/2104; 0.1–0.5) | 86.7 (26/30; 70.3–94.7) | professor: 14, unparsed: 4, rapper: 2 |
| professor | female | 61.3 (166/271; 55.3–66.9) | 2.4 (37/1572; 1.7–3.2) | 81.8 (166/203; 75.9–86.5) | physician: 21, unparsed: 15, psychologist: 14 |
| professor | male | 59.3 (195/329; 53.9–64.4) | 5.6 (103/1826; 4.7–6.8) | 65.4 (195/298; 59.9–70.6) | physician: 42, software_engineer: 28, unparsed: 16 |
| psychologist | female | 68.8 (44/64; 56.6–78.8) | 1.0 (18/1779; 0.6–1.6) | 71.0 (44/62; 58.7–80.8) | professor: 6, attorney: 3, unparsed: 3 |
| psychologist | male | 61.5 (24/39; 45.9–75.1) | 0.5 (11/2116; 0.3–0.9) | 68.6 (24/35; 52.0–81.4) | professor: 10, paralegal: 1, journalist: 1 |
| rapper | female | 60.0 (6/10; 31.3–83.2) | 0.1 (1/1833; 0.0–0.3) | 85.7 (6/7; 48.7–97.4) | unparsed: 3, comedian: 1 |
| rapper | male | 74.4 (67/90; 64.6–82.3) | 0.3 (6/2065; 0.1–0.6) | 91.8 (67/73; 83.2–96.2) | dj: 9, comedian: 6, unparsed: 3 |
| software_engineer | female | 87.5 (14/16; 64.0–96.5) | 0.7 (12/1827; 0.4–1.1) | 53.8 (14/26; 35.5–71.2) | attorney: 1, professor: 1 |
| software_engineer | male | 83.3 (70/84; 73.9–89.8) | 3.5 (73/2071; 2.8–4.4) | 49.0 (70/143; 40.9–57.1) | professor: 5, teacher: 2, architect: 2 |
| surgeon | female | 17.6 (3/17; 6.2–41.0) | 0.1 (2/1826; 0.0–0.4) | 60.0 (3/5; 23.1–88.2) | physician: 12, dentist: 1, professor: 1 |
| surgeon | male | 25.3 (25/99; 17.7–34.6) | 0.4 (8/2056; 0.2–0.8) | 75.8 (25/33; 59.0–87.2) | physician: 64, professor: 5, dentist: 3 |
| teacher | female | 55.4 (46/83; 44.7–65.6) | 3.3 (58/1760; 2.6–4.2) | 44.2 (46/104; 35.1–53.8) | unparsed: 7, professor: 6, pastor: 4 |
| teacher | male | 41.8 (23/55; 29.7–55.0) | 1.0 (22/2100; 0.7–1.6) | 51.1 (23/45; 37.0–65.0) | professor: 15, composer: 4, unparsed: 4 |
| yoga_teacher | female | 90.5 (76/84; 82.3–95.1) | 0.5 (8/1759; 0.2–0.9) | 90.5 (76/84; 82.3–95.1) | teacher: 3, personal_trainer: 2, photographer: 1 |
| yoga_teacher | male | 56.2 (9/16; 33.2–76.9) | 0.1 (2/2139; 0.0–0.3) | 81.8 (9/11; 52.3–94.9) | unparsed: 2, journalist: 1, professor: 1 |

## 1_original

| Occupation | Gender | TPR | FPR | Precision | Top three error destinations |
|---|---|---|---|---|---|
| accountant | female | 81.1 (30/37; 65.8–90.5) | 1.9 (35/1806; 1.4–2.7) | 46.2 (30/65; 34.6–58.1) | journalist: 3, physician: 2, model: 1 |
| accountant | male | 79.4 (50/63; 67.8–87.5) | 0.9 (18/2092; 0.5–1.4) | 73.5 (50/68; 62.0–82.6) | journalist: 4, attorney: 2, pastor: 2 |
| architect | female | 75.0 (18/24; 55.1–88.0) | 0.3 (5/1819; 0.1–0.6) | 78.3 (18/23; 58.1–90.3) | interior_designer: 3, software_engineer: 1, accountant: 1 |
| architect | male | 59.0 (46/78; 47.9–69.2) | 0.5 (10/2077; 0.3–0.9) | 82.1 (46/56; 70.2–90.0) | software_engineer: 14, professor: 5, interior_designer: 3 |
| attorney | female | 89.6 (69/77; 80.8–94.6) | 1.4 (24/1766; 0.9–2.0) | 74.2 (69/93; 64.5–82.0) | accountant: 3, professor: 2, interior_designer: 1 |
| attorney | male | 88.8 (111/125; 82.1–93.2) | 0.5 (10/2030; 0.3–0.9) | 91.7 (111/121; 85.5–95.4) | accountant: 5, journalist: 2, professor: 2 |
| chiropractor | female | 76.9 (20/26; 57.9–89.0) | 0.2 (3/1817; 0.1–0.5) | 87.0 (20/23; 67.9–95.5) | physician: 4, accountant: 1, personal_trainer: 1 |
| chiropractor | male | 81.1 (60/74; 70.7–88.4) | 0.3 (6/2081; 0.1–0.6) | 90.9 (60/66; 81.6–95.8) | physician: 7, dentist: 3, pastor: 1 |
| comedian | female | 95.2 (20/21; 77.3–99.2) | 0.3 (5/1822; 0.1–0.6) | 80.0 (20/25; 60.9–91.1) | journalist: 1 |
| comedian | male | 97.5 (77/79; 91.2–99.3) | 0.8 (16/2076; 0.5–1.2) | 82.8 (77/93; 73.9–89.1) | dj: 1, poet: 1 |
| composer | female | 81.2 (13/16; 57.0–93.4) | 0.0 (0/1827; 0.0–0.2) | 100.0 (13/13; 77.2–100.0) | comedian: 1, professor: 1, teacher: 1 |
| composer | male | 94.0 (79/84; 86.8–97.4) | 0.4 (9/2071; 0.2–0.8) | 89.8 (79/88; 81.7–94.5) | rapper: 1, architect: 1, teacher: 1 |
| dentist | female | 92.2 (47/51; 81.5–96.9) | 0.2 (3/1792; 0.1–0.5) | 94.0 (47/50; 83.8–97.9) | physician: 2, journalist: 1, surgeon: 1 |
| dentist | male | 93.7 (89/95; 86.9–97.1) | 0.3 (7/2060; 0.2–0.7) | 92.7 (89/96; 85.7–96.4) | chiropractor: 3, photographer: 1, physician: 1 |
| dietitian | female | 89.2 (83/93; 81.3–94.1) | 0.2 (3/1750; 0.1–0.5) | 96.5 (83/86; 90.2–98.8) | accountant: 2, physician: 1, personal_trainer: 1 |
| dietitian | male | 71.4 (5/7; 35.9–91.8) | 0.0 (0/2148; 0.0–0.2) | 100.0 (5/5; 56.6–100.0) | personal_trainer: 1, physician: 1 |
| dj | female | 71.4 (10/14; 45.4–88.3) | 0.0 (0/1829; 0.0–0.2) | 100.0 (10/10; 72.2–100.0) | rapper: 1, model: 1, accountant: 1 |
| dj | male | 86.0 (74/86; 77.2–91.8) | 0.2 (5/2069; 0.1–0.6) | 93.7 (74/79; 86.0–97.3) | rapper: 4, comedian: 2, photographer: 1 |
| filmmaker | female | 90.9 (30/33; 76.4–96.9) | 0.2 (3/1810; 0.1–0.5) | 90.9 (30/33; 76.4–96.9) | psychologist: 1, journalist: 1, teacher: 1 |
| filmmaker | male | 92.5 (62/67; 83.7–96.8) | 0.2 (4/2088; 0.1–0.5) | 93.9 (62/66; 85.4–97.6) | journalist: 2, photographer: 1, comedian: 1 |
| interior_designer | female | 84.0 (68/81; 74.5–90.4) | 0.3 (6/1762; 0.2–0.7) | 91.9 (68/74; 83.4–96.2) | architect: 3, photographer: 2, model: 2 |
| interior_designer | male | 84.2 (16/19; 62.4–94.5) | 0.1 (3/2136; 0.0–0.4) | 84.2 (16/19; 62.4–94.5) | architect: 2, attorney: 1 |
| journalist | female | 82.8 (82/99; 74.2–89.0) | 1.4 (25/1744; 1.0–2.1) | 76.6 (82/107; 67.8–83.6) | photographer: 3, accountant: 3, attorney: 2 |
| journalist | male | 88.2 (90/102; 80.6–93.1) | 1.3 (27/2053; 0.9–1.9) | 76.9 (90/117; 68.5–83.6) | professor: 5, photographer: 3, comedian: 2 |
| model | female | 85.5 (71/83; 76.4–91.5) | 0.3 (6/1760; 0.2–0.7) | 92.2 (71/77; 84.0–96.4) | accountant: 2, photographer: 2, teacher: 2 |
| model | male | 70.6 (12/17; 46.9–86.7) | 0.0 (1/2138; 0.0–0.3) | 92.3 (12/13; 66.7–98.6) | professor: 2, teacher: 2, attorney: 1 |
| nurse | female | 83.3 (145/174; 77.1–88.1) | 0.8 (14/1669; 0.5–1.4) | 91.2 (145/159; 85.8–94.7) | physician: 10, professor: 5, accountant: 3 |
| nurse | male | 70.6 (12/17; 46.9–86.7) | 0.0 (1/2138; 0.0–0.3) | 92.3 (12/13; 66.7–98.6) | physician: 3, psychologist: 1, comedian: 1 |
| painter | female | 80.4 (37/46; 66.8–89.3) | 0.4 (7/1797; 0.2–0.8) | 84.1 (37/44; 70.6–92.1) | photographer: 4, poet: 2, professor: 1 |
| painter | male | 85.2 (46/54; 73.4–92.3) | 0.1 (3/2101; 0.0–0.4) | 93.9 (46/49; 83.5–97.9) | photographer: 3, professor: 2, unparsed: 1 |
| paralegal | female | 72.9 (62/85; 62.7–81.2) | 0.1 (2/1758; 0.0–0.4) | 96.9 (62/64; 89.3–99.1) | attorney: 17, accountant: 3, journalist: 2 |
| paralegal | male | 66.7 (10/15; 41.7–84.8) | 0.0 (0/2140; 0.0–0.2) | 100.0 (10/10; 72.2–100.0) | attorney: 4, accountant: 1 |
| pastor | female | 91.7 (22/24; 74.2–97.7) | 0.1 (2/1819; 0.0–0.4) | 91.7 (22/24; 74.2–97.7) | yoga_teacher: 1, accountant: 1 |
| pastor | male | 82.9 (63/76; 72.9–89.7) | 0.4 (8/2079; 0.2–0.8) | 88.7 (63/71; 79.3–94.2) | accountant: 4, journalist: 3, comedian: 2 |
| personal_trainer | female | 91.3 (42/46; 79.7–96.6) | 0.1 (2/1797; 0.0–0.4) | 95.5 (42/44; 84.9–98.7) | accountant: 2, journalist: 1, yoga_teacher: 1 |
| personal_trainer | male | 96.2 (51/53; 87.2–99.0) | 0.1 (2/2102; 0.0–0.3) | 96.2 (51/53; 87.2–99.0) | teacher: 1, model: 1 |
| photographer | female | 91.5 (65/71; 82.8–96.1) | 0.9 (16/1772; 0.6–1.5) | 80.2 (65/81; 70.3–87.5) | painter: 2, architect: 1, dietitian: 1 |
| photographer | male | 95.3 (123/129; 90.2–97.9) | 0.9 (18/2026; 0.6–1.4) | 87.2 (123/141; 80.7–91.8) | journalist: 2, filmmaker: 1, accountant: 1 |
| physician | female | 91.2 (135/148; 85.6–94.8) | 1.4 (24/1695; 1.0–2.1) | 84.9 (135/159; 78.5–89.6) | surgeon: 4, nurse: 4, dentist: 2 |
| physician | male | 78.3 (119/152; 71.1–84.1) | 1.7 (34/2003; 1.2–2.4) | 77.8 (119/153; 70.6–83.6) | professor: 12, surgeon: 11, chiropractor: 3 |
| poet | female | 85.7 (42/49; 73.3–92.9) | 0.4 (7/1794; 0.2–0.8) | 85.7 (42/49; 73.3–92.9) | journalist: 3, comedian: 1, professor: 1 |
| poet | male | 70.6 (36/51; 57.0–81.3) | 0.4 (8/2104; 0.2–0.7) | 81.8 (36/44; 68.0–90.5) | journalist: 5, rapper: 5, professor: 3 |
| professor | female | 93.7 (254/271; 90.2–96.0) | 2.0 (31/1572; 1.4–2.8) | 89.1 (254/285; 85.0–92.2) | teacher: 6, psychologist: 2, nurse: 2 |
| professor | male | 90.9 (299/329; 87.3–93.5) | 3.0 (54/1826; 2.3–3.8) | 84.7 (299/353; 80.6–88.1) | physician: 5, surgeon: 5, journalist: 3 |
| psychologist | female | 68.8 (44/64; 56.6–78.8) | 0.3 (6/1779; 0.2–0.7) | 88.0 (44/50; 76.2–94.4) | professor: 10, nurse: 2, teacher: 2 |
| psychologist | male | 74.4 (29/39; 58.9–85.4) | 0.2 (5/2116; 0.1–0.6) | 85.3 (29/34; 69.9–93.6) | professor: 4, journalist: 2, teacher: 1 |
| rapper | female | 90.0 (9/10; 59.6–98.2) | 0.1 (2/1833; 0.0–0.4) | 81.8 (9/11; 52.3–94.9) | painter: 1 |
| rapper | male | 94.4 (85/90; 87.6–97.6) | 0.5 (10/2065; 0.3–0.9) | 89.5 (85/95; 81.7–94.2) | dj: 2, poet: 2, comedian: 1 |
| software_engineer | female | 87.5 (14/16; 64.0–96.5) | 0.1 (2/1827; 0.0–0.4) | 87.5 (14/16; 64.0–96.5) | accountant: 1, professor: 1 |
| software_engineer | male | 88.1 (74/84; 79.5–93.4) | 1.0 (21/2071; 0.7–1.5) | 77.9 (74/95; 68.6–85.1) | architect: 2, accountant: 1, unparsed: 1 |
| surgeon | female | 70.6 (12/17; 46.9–86.7) | 0.3 (5/1826; 0.1–0.6) | 70.6 (12/17; 46.9–86.7) | physician: 3, dentist: 1, accountant: 1 |
| surgeon | male | 72.7 (72/99; 63.2–80.5) | 0.8 (17/2056; 0.5–1.3) | 80.9 (72/89; 71.5–87.7) | physician: 14, professor: 6, dentist: 4 |
| teacher | female | 55.4 (46/83; 44.7–65.6) | 0.9 (16/1760; 0.6–1.5) | 74.2 (46/62; 62.1–83.4) | accountant: 7, yoga_teacher: 5, professor: 5 |
| teacher | male | 65.5 (36/55; 52.3–76.6) | 0.4 (8/2100; 0.2–0.7) | 81.8 (36/44; 68.0–90.5) | professor: 6, pastor: 2, yoga_teacher: 2 |
| yoga_teacher | female | 97.6 (82/84; 91.7–99.3) | 0.6 (11/1759; 0.3–1.1) | 88.2 (82/93; 80.1–93.3) | photographer: 1, comedian: 1 |
| yoga_teacher | male | 75.0 (12/16; 50.5–89.8) | 0.2 (4/2139; 0.1–0.5) | 75.0 (12/16; 50.5–89.8) | software_engineer: 1, professor: 1, poet: 1 |

## GPT-generated-data-GPT-filtering-full__2_original_all

| Occupation | Gender | TPR | FPR | Precision | Top three error destinations |
|---|---|---|---|---|---|
| accountant | female | 73.0 (27/37; 57.0–84.6) | 0.7 (13/1806; 0.4–1.2) | 67.5 (27/40; 52.0–79.9) | model: 2, physician: 2, psychologist: 1 |
| accountant | male | 73.0 (46/63; 61.0–82.4) | 0.3 (7/2092; 0.2–0.7) | 86.8 (46/53; 75.2–93.5) | pastor: 4, model: 3, journalist: 2 |
| architect | female | 70.8 (17/24; 50.8–85.1) | 0.4 (7/1819; 0.2–0.8) | 70.8 (17/24; 50.8–85.1) | interior_designer: 3, software_engineer: 2, accountant: 1 |
| architect | male | 69.2 (54/78; 58.3–78.4) | 0.8 (16/2077; 0.5–1.2) | 77.1 (54/70; 66.0–85.4) | software_engineer: 11, professor: 6, journalist: 2 |
| attorney | female | 89.6 (69/77; 80.8–94.6) | 1.2 (21/1766; 0.8–1.8) | 76.7 (69/90; 66.9–84.2) | accountant: 3, professor: 2, model: 1 |
| attorney | male | 89.6 (112/125; 83.0–93.8) | 0.3 (6/2030; 0.1–0.6) | 94.9 (112/118; 89.3–97.6) | professor: 4, accountant: 2, journalist: 2 |
| chiropractor | female | 73.1 (19/26; 53.9–86.3) | 0.2 (4/1817; 0.1–0.6) | 82.6 (19/23; 62.9–93.0) | physician: 5, teacher: 1, personal_trainer: 1 |
| chiropractor | male | 83.8 (62/74; 73.8–90.5) | 0.4 (8/2081; 0.2–0.8) | 88.6 (62/70; 79.0–94.1) | physician: 3, dietitian: 2, pastor: 1 |
| comedian | female | 81.0 (17/21; 60.0–92.3) | 0.2 (4/1822; 0.1–0.6) | 81.0 (17/21; 60.0–92.3) | nurse: 1, dj: 1, journalist: 1 |
| comedian | male | 92.4 (73/79; 84.4–96.5) | 0.3 (6/2076; 0.1–0.6) | 92.4 (73/79; 84.4–96.5) | dj: 4, poet: 1, surgeon: 1 |
| composer | female | 81.2 (13/16; 57.0–93.4) | 0.0 (0/1827; 0.0–0.2) | 100.0 (13/13; 77.2–100.0) | comedian: 1, professor: 1, teacher: 1 |
| composer | male | 95.2 (80/84; 88.4–98.1) | 0.3 (7/2071; 0.2–0.7) | 92.0 (80/87; 84.3–96.0) | dj: 2, model: 1, architect: 1 |
| dentist | female | 74.5 (38/51; 61.1–84.5) | 0.1 (1/1792; 0.0–0.3) | 97.4 (38/39; 86.8–99.5) | surgeon: 11, professor: 1, pastor: 1 |
| dentist | male | 64.2 (61/95; 54.2–73.1) | 0.2 (4/2060; 0.1–0.5) | 93.8 (61/65; 85.2–97.6) | surgeon: 27, chiropractor: 4, photographer: 1 |
| dietitian | female | 94.6 (88/93; 88.0–97.7) | 0.5 (8/1750; 0.2–0.9) | 91.7 (88/96; 84.4–95.7) | accountant: 2, physician: 1, chiropractor: 1 |
| dietitian | male | 85.7 (6/7; 48.7–97.4) | 0.1 (2/2148; 0.0–0.3) | 75.0 (6/8; 40.9–92.9) | physician: 1 |
| dj | female | 92.9 (13/14; 68.5–98.7) | 0.1 (1/1829; 0.0–0.3) | 92.9 (13/14; 68.5–98.7) | model: 1 |
| dj | male | 89.5 (77/86; 81.3–94.4) | 0.9 (19/2069; 0.6–1.4) | 80.2 (77/96; 71.1–86.9) | rapper: 2, comedian: 2, personal_trainer: 1 |
| filmmaker | female | 87.9 (29/33; 72.7–95.2) | 0.3 (5/1810; 0.1–0.6) | 85.3 (29/34; 69.9–93.6) | psychologist: 2, journalist: 1, teacher: 1 |
| filmmaker | male | 89.6 (60/67; 80.0–94.8) | 0.3 (6/2088; 0.1–0.6) | 90.9 (60/66; 81.6–95.8) | photographer: 2, journalist: 2, professor: 2 |
| interior_designer | female | 85.2 (69/81; 75.9–91.3) | 0.7 (13/1762; 0.4–1.3) | 84.1 (69/82; 74.7–90.5) | architect: 4, model: 3, accountant: 1 |
| interior_designer | male | 73.7 (14/19; 51.2–88.2) | 0.0 (1/2136; 0.0–0.3) | 93.3 (14/15; 70.2–98.8) | architect: 4, attorney: 1 |
| journalist | female | 82.8 (82/99; 74.2–89.0) | 0.6 (10/1744; 0.3–1.1) | 89.1 (82/92; 81.1–94.0) | model: 3, photographer: 3, filmmaker: 2 |
| journalist | male | 84.3 (86/102; 76.0–90.1) | 0.9 (19/2053; 0.6–1.4) | 81.9 (86/105; 73.5–88.1) | professor: 7, photographer: 2, teacher: 1 |
| model | female | 88.0 (73/83; 79.2–93.3) | 1.0 (17/1760; 0.6–1.5) | 81.1 (73/90; 71.8–87.9) | journalist: 2, personal_trainer: 1, comedian: 1 |
| model | male | 88.2 (15/17; 65.7–96.7) | 0.6 (12/2138; 0.3–1.0) | 55.6 (15/27; 37.3–72.4) | professor: 2 |
| nurse | female | 80.5 (140/174; 73.9–85.7) | 0.6 (10/1669; 0.3–1.1) | 93.3 (140/150; 88.2–96.3) | physician: 17, professor: 5, model: 4 |
| nurse | male | 70.6 (12/17; 46.9–86.7) | 0.0 (1/2138; 0.0–0.3) | 92.3 (12/13; 66.7–98.6) | physician: 3, psychologist: 1, chiropractor: 1 |
| painter | female | 91.3 (42/46; 79.7–96.6) | 0.4 (8/1797; 0.2–0.9) | 84.0 (42/50; 71.5–91.7) | poet: 1, interior_designer: 1, filmmaker: 1 |
| painter | male | 87.0 (47/54; 75.6–93.6) | 0.3 (6/2101; 0.1–0.6) | 88.7 (47/53; 77.4–94.7) | photographer: 3, unparsed: 1, software_engineer: 1 |
| paralegal | female | 76.5 (65/85; 66.4–84.2) | 0.1 (2/1758; 0.0–0.4) | 97.0 (65/67; 89.8–99.2) | attorney: 16, accountant: 1, journalist: 1 |
| paralegal | male | 66.7 (10/15; 41.7–84.8) | 0.0 (1/2140; 0.0–0.3) | 90.9 (10/11; 62.3–98.4) | attorney: 3, accountant: 1, unparsed: 1 |
| pastor | female | 95.8 (23/24; 79.8–99.3) | 0.5 (9/1819; 0.3–0.9) | 71.9 (23/32; 54.6–84.4) | interior_designer: 1 |
| pastor | male | 86.8 (66/76; 77.4–92.7) | 0.6 (12/2079; 0.3–1.0) | 84.6 (66/78; 75.0–91.0) | journalist: 2, teacher: 2, dj: 1 |
| personal_trainer | female | 89.1 (41/46; 77.0–95.3) | 0.2 (3/1797; 0.1–0.5) | 93.2 (41/44; 81.8–97.7) | journalist: 1, pastor: 1, psychologist: 1 |
| personal_trainer | male | 88.7 (47/53; 77.4–94.7) | 0.1 (3/2102; 0.0–0.4) | 94.0 (47/50; 83.8–97.9) | surgeon: 2, model: 2, teacher: 1 |
| photographer | female | 87.3 (62/71; 77.6–93.2) | 0.4 (7/1772; 0.2–0.8) | 89.9 (62/69; 80.5–95.0) | painter: 3, architect: 2, dietitian: 2 |
| photographer | male | 92.2 (119/129; 86.3–95.7) | 0.6 (12/2026; 0.3–1.0) | 90.8 (119/131; 84.7–94.7) | painter: 3, model: 2, journalist: 1 |
| physician | female | 93.2 (138/148; 88.0–96.3) | 1.9 (32/1695; 1.3–2.7) | 81.2 (138/170; 74.6–86.3) | nurse: 4, surgeon: 2, professor: 2 |
| physician | male | 83.6 (127/152; 76.8–88.6) | 1.5 (30/2003; 1.1–2.1) | 80.9 (127/157; 74.0–86.3) | surgeon: 16, professor: 5, psychologist: 2 |
| poet | female | 83.7 (41/49; 71.0–91.5) | 0.4 (8/1794; 0.2–0.9) | 83.7 (41/49; 71.0–91.5) | painter: 2, professor: 2, comedian: 1 |
| poet | male | 76.5 (39/51; 63.2–86.0) | 0.2 (4/2104; 0.1–0.5) | 90.7 (39/43; 78.4–96.3) | rapper: 4, journalist: 3, professor: 2 |
| professor | female | 91.5 (248/271; 87.6–94.3) | 1.8 (29/1572; 1.3–2.6) | 89.5 (248/277; 85.4–92.6) | teacher: 7, physician: 5, poet: 2 |
| professor | male | 90.0 (296/329; 86.2–92.8) | 2.7 (49/1826; 2.0–3.5) | 85.8 (296/345; 81.7–89.1) | surgeon: 7, physician: 7, psychologist: 4 |
| psychologist | female | 81.2 (52/64; 70.0–88.9) | 0.4 (8/1779; 0.2–0.9) | 86.7 (52/60; 75.8–93.1) | professor: 7, attorney: 2, surgeon: 1 |
| psychologist | male | 74.4 (29/39; 58.9–85.4) | 0.6 (12/2116; 0.3–1.0) | 70.7 (29/41; 55.5–82.4) | professor: 5, unparsed: 1, teacher: 1 |
| rapper | female | 90.0 (9/10; 59.6–98.2) | 0.0 (0/1833; 0.0–0.2) | 100.0 (9/9; 70.1–100.0) | painter: 1 |
| rapper | male | 87.8 (79/90; 79.4–93.0) | 0.3 (6/2065; 0.1–0.6) | 92.9 (79/85; 85.4–96.7) | dj: 8, poet: 2, comedian: 1 |
| software_engineer | female | 87.5 (14/16; 64.0–96.5) | 0.3 (5/1827; 0.1–0.6) | 73.7 (14/19; 51.2–88.2) | professor: 1, architect: 1 |
| software_engineer | male | 83.3 (70/84; 73.9–89.8) | 0.7 (15/2071; 0.4–1.2) | 82.4 (70/85; 72.9–89.0) | architect: 5, professor: 4, accountant: 1 |
| surgeon | female | 76.5 (13/17; 52.7–90.4) | 0.9 (17/1826; 0.6–1.5) | 43.3 (13/30; 27.4–60.8) | physician: 2, model: 1, chiropractor: 1 |
| surgeon | male | 82.8 (82/99; 74.2–89.0) | 2.7 (55/2056; 2.1–3.5) | 59.9 (82/137; 51.5–67.7) | physician: 10, dentist: 3, professor: 1 |
| teacher | female | 62.7 (52/83; 51.9–72.3) | 0.9 (16/1760; 0.6–1.5) | 76.5 (52/68; 65.1–85.0) | yoga_teacher: 6, pastor: 4, professor: 4 |
| teacher | male | 61.8 (34/55; 48.6–73.5) | 0.6 (12/2100; 0.3–1.0) | 73.9 (34/46; 59.7–84.4) | professor: 7, model: 3, composer: 2 |
| yoga_teacher | female | 96.4 (81/84; 90.0–98.8) | 0.4 (7/1759; 0.2–0.8) | 92.0 (81/88; 84.5–96.1) | personal_trainer: 1, comedian: 1, chiropractor: 1 |
| yoga_teacher | male | 87.5 (14/16; 64.0–96.5) | 0.1 (3/2139; 0.0–0.4) | 82.4 (14/17; 59.0–93.8) | teacher: 1, physician: 1 |

## GPT-generated-data-GPT-filtering-full__3_original_content_only

| Occupation | Gender | TPR | FPR | Precision | Top three error destinations |
|---|---|---|---|---|---|
| accountant | female | 70.3 (26/37; 54.2–82.5) | 0.2 (3/1806; 0.1–0.5) | 89.7 (26/29; 73.6–96.4) | interior_designer: 2, nurse: 2, teacher: 2 |
| accountant | male | 69.8 (44/63; 57.6–79.8) | 0.3 (7/2092; 0.2–0.7) | 86.3 (44/51; 74.3–93.2) | attorney: 5, journalist: 4, pastor: 4 |
| architect | female | 58.3 (14/24; 38.8–75.5) | 0.3 (5/1819; 0.1–0.6) | 73.7 (14/19; 51.2–88.2) | interior_designer: 4, software_engineer: 3, professor: 2 |
| architect | male | 75.6 (59/78; 65.1–83.8) | 0.8 (16/2077; 0.5–1.2) | 78.7 (59/75; 68.1–86.4) | interior_designer: 5, software_engineer: 3, professor: 2 |
| attorney | female | 85.7 (66/77; 76.2–91.8) | 0.6 (10/1766; 0.3–1.0) | 86.8 (66/76; 77.4–92.7) | paralegal: 4, nurse: 2, professor: 1 |
| attorney | male | 89.6 (112/125; 83.0–93.8) | 0.6 (13/2030; 0.4–1.1) | 89.6 (112/125; 83.0–93.8) | journalist: 2, unparsed: 2, accountant: 2 |
| chiropractor | female | 57.7 (15/26; 38.9–74.5) | 0.1 (2/1817; 0.0–0.4) | 88.2 (15/17; 65.7–96.7) | nurse: 4, physician: 3, dentist: 2 |
| chiropractor | male | 77.0 (57/74; 66.3–85.1) | 0.6 (13/2081; 0.4–1.1) | 81.4 (57/70; 70.8–88.8) | physician: 9, surgeon: 3, pastor: 1 |
| comedian | female | 76.2 (16/21; 54.9–89.4) | 0.3 (5/1822; 0.1–0.6) | 76.2 (16/21; 54.9–89.4) | nurse: 2, journalist: 2, model: 1 |
| comedian | male | 97.5 (77/79; 91.2–99.3) | 0.2 (5/2076; 0.1–0.6) | 93.9 (77/82; 86.5–97.4) | composer: 1, journalist: 1 |
| composer | female | 87.5 (14/16; 64.0–96.5) | 0.0 (0/1827; 0.0–0.2) | 100.0 (14/14; 78.5–100.0) | comedian: 1, teacher: 1 |
| composer | male | 97.6 (82/84; 91.7–99.3) | 0.5 (11/2071; 0.3–0.9) | 88.2 (82/93; 80.1–93.3) | interior_designer: 1, dj: 1 |
| dentist | female | 90.2 (46/51; 79.0–95.7) | 0.2 (4/1792; 0.1–0.6) | 92.0 (46/50; 81.2–96.8) | surgeon: 2, physician: 1, nurse: 1 |
| dentist | male | 89.5 (85/95; 81.7–94.2) | 0.1 (3/2060; 0.0–0.4) | 96.6 (85/88; 90.5–98.8) | chiropractor: 4, surgeon: 3, photographer: 1 |
| dietitian | female | 91.4 (85/93; 83.9–95.6) | 0.2 (3/1750; 0.1–0.5) | 96.6 (85/88; 90.5–98.8) | nurse: 3, physician: 1, personal_trainer: 1 |
| dietitian | male | 85.7 (6/7; 48.7–97.4) | 0.0 (0/2148; 0.0–0.2) | 100.0 (6/6; 61.0–100.0) | physician: 1 |
| dj | female | 78.6 (11/14; 52.4–92.4) | 0.0 (0/1829; 0.0–0.2) | 100.0 (11/11; 74.1–100.0) | model: 2, comedian: 1 |
| dj | male | 89.5 (77/86; 81.3–94.4) | 0.4 (8/2069; 0.2–0.8) | 90.6 (77/85; 82.5–95.2) | rapper: 2, personal_trainer: 1, poet: 1 |
| filmmaker | female | 87.9 (29/33; 72.7–95.2) | 0.1 (2/1810; 0.0–0.4) | 93.5 (29/31; 79.3–98.2) | psychologist: 1, nurse: 1, journalist: 1 |
| filmmaker | male | 88.1 (59/67; 78.2–93.8) | 0.1 (2/2088; 0.0–0.3) | 96.7 (59/61; 88.8–99.1) | journalist: 3, photographer: 2, painter: 1 |
| interior_designer | female | 87.7 (71/81; 78.7–93.2) | 0.9 (15/1762; 0.5–1.4) | 82.6 (71/86; 73.2–89.1) | model: 4, journalist: 2, nurse: 1 |
| interior_designer | male | 89.5 (17/19; 68.6–97.1) | 0.4 (8/2136; 0.2–0.7) | 68.0 (17/25; 48.4–82.8) | attorney: 1, architect: 1 |
| journalist | female | 84.8 (84/99; 76.5–90.6) | 1.3 (22/1744; 0.8–1.9) | 79.2 (84/106; 70.6–85.9) | model: 4, teacher: 2, photographer: 2 |
| journalist | male | 91.2 (93/102; 84.1–95.3) | 1.2 (25/2053; 0.8–1.8) | 78.8 (93/118; 70.6–85.2) | professor: 2, comedian: 1, psychologist: 1 |
| model | female | 88.0 (73/83; 79.2–93.3) | 0.9 (16/1760; 0.6–1.5) | 82.0 (73/89; 72.8–88.6) | journalist: 3, interior_designer: 2, teacher: 2 |
| model | male | 88.2 (15/17; 65.7–96.7) | 0.4 (9/2138; 0.2–0.8) | 62.5 (15/24; 42.7–78.8) | professor: 1, teacher: 1 |
| nurse | female | 91.4 (159/174; 86.3–94.7) | 2.6 (43/1669; 1.9–3.5) | 78.7 (159/202; 72.6–83.8) | professor: 5, unparsed: 3, journalist: 2 |
| nurse | male | 70.6 (12/17; 46.9–86.7) | 0.2 (4/2138; 0.1–0.5) | 75.0 (12/16; 50.5–89.8) | physician: 2, psychologist: 1, chiropractor: 1 |
| painter | female | 89.1 (41/46; 77.0–95.3) | 0.3 (6/1797; 0.2–0.7) | 87.2 (41/47; 74.8–94.0) | photographer: 3, poet: 1, interior_designer: 1 |
| painter | male | 83.3 (45/54; 71.3–91.0) | 0.3 (6/2101; 0.1–0.6) | 88.2 (45/51; 76.6–94.5) | photographer: 4, unparsed: 2, poet: 1 |
| paralegal | female | 87.1 (74/85; 78.3–92.6) | 0.3 (6/1758; 0.2–0.7) | 92.5 (74/80; 84.6–96.5) | attorney: 7, nurse: 2, journalist: 1 |
| paralegal | male | 66.7 (10/15; 41.7–84.8) | 0.0 (0/2140; 0.0–0.2) | 100.0 (10/10; 72.2–100.0) | attorney: 3, accountant: 1, unparsed: 1 |
| pastor | female | 91.7 (22/24; 74.2–97.7) | 0.4 (7/1819; 0.2–0.8) | 75.9 (22/29; 57.9–87.8) | teacher: 1, interior_designer: 1 |
| pastor | male | 90.8 (69/76; 82.2–95.5) | 0.6 (12/2079; 0.3–1.0) | 85.2 (69/81; 75.9–91.3) | journalist: 2, teacher: 1, composer: 1 |
| personal_trainer | female | 89.1 (41/46; 77.0–95.3) | 0.5 (9/1797; 0.3–0.9) | 82.0 (41/50; 69.2–90.2) | nurse: 1, pastor: 1, model: 1 |
| personal_trainer | male | 94.3 (50/53; 84.6–98.1) | 0.2 (5/2102; 0.1–0.6) | 90.9 (50/55; 80.4–96.1) | nurse: 1, surgeon: 1, model: 1 |
| photographer | female | 93.0 (66/71; 84.6–97.0) | 0.6 (11/1772; 0.3–1.1) | 85.7 (66/77; 76.2–91.8) | architect: 1, dietitian: 1, model: 1 |
| photographer | male | 93.0 (120/129; 87.3–96.3) | 0.7 (15/2026; 0.4–1.2) | 88.9 (120/135; 82.5–93.1) | model: 3, journalist: 2, painter: 1 |
| physician | female | 84.5 (125/148; 77.8–89.4) | 0.8 (13/1695; 0.4–1.3) | 90.6 (125/138; 84.5–94.4) | nurse: 10, surgeon: 9, professor: 3 |
| physician | male | 64.5 (98/152; 56.6–71.6) | 1.5 (30/2003; 1.1–2.1) | 76.6 (98/128; 68.5–83.1) | surgeon: 37, chiropractor: 8, professor: 6 |
| poet | female | 85.7 (42/49; 73.3–92.9) | 0.3 (5/1794; 0.1–0.7) | 89.4 (42/47; 77.4–95.4) | painter: 2, journalist: 2, comedian: 1 |
| poet | male | 76.5 (39/51; 63.2–86.0) | 0.3 (6/2104; 0.1–0.6) | 86.7 (39/45; 73.8–93.7) | journalist: 5, rapper: 4, model: 1 |
| professor | female | 89.7 (243/271; 85.5–92.8) | 1.5 (24/1572; 1.0–2.3) | 91.0 (243/267; 87.0–93.9) | teacher: 5, journalist: 5, psychologist: 4 |
| professor | male | 88.4 (291/329; 84.5–91.5) | 1.5 (28/1826; 1.1–2.2) | 91.2 (291/319; 87.6–93.9) | surgeon: 8, physician: 5, journalist: 4 |
| psychologist | female | 73.4 (47/64; 61.5–82.7) | 0.3 (6/1779; 0.2–0.7) | 88.7 (47/53; 77.4–94.7) | professor: 6, nurse: 3, yoga_teacher: 2 |
| psychologist | male | 79.5 (31/39; 64.5–89.2) | 0.3 (7/2116; 0.2–0.7) | 81.6 (31/38; 66.6–90.8) | teacher: 2, professor: 2, personal_trainer: 1 |
| rapper | female | 90.0 (9/10; 59.6–98.2) | 0.0 (0/1833; 0.0–0.2) | 100.0 (9/9; 70.1–100.0) | painter: 1 |
| rapper | male | 92.2 (83/90; 84.8–96.2) | 0.3 (6/2065; 0.1–0.6) | 93.3 (83/89; 86.1–96.9) | dj: 4, poet: 2, model: 1 |
| software_engineer | female | 81.2 (13/16; 57.0–93.4) | 0.3 (5/1827; 0.1–0.6) | 72.2 (13/18; 49.1–87.5) | architect: 2, professor: 1 |
| software_engineer | male | 75.0 (63/84; 64.8–83.0) | 0.4 (9/2071; 0.2–0.8) | 87.5 (63/72; 77.9–93.3) | architect: 9, professor: 4, accountant: 1 |
| surgeon | female | 70.6 (12/17; 46.9–86.7) | 0.8 (14/1826; 0.5–1.3) | 46.2 (12/26; 28.8–64.5) | physician: 2, dentist: 1, nurse: 1 |
| surgeon | male | 87.9 (87/99; 80.0–92.9) | 2.6 (53/2056; 2.0–3.4) | 62.1 (87/140; 53.9–69.8) | physician: 5, dentist: 3, nurse: 2 |
| teacher | female | 60.2 (50/83; 49.5–70.1) | 1.1 (19/1760; 0.7–1.7) | 72.5 (50/69; 61.0–81.6) | nurse: 6, pastor: 4, yoga_teacher: 3 |
| teacher | male | 65.5 (36/55; 52.3–76.6) | 0.4 (8/2100; 0.2–0.7) | 81.8 (36/44; 68.0–90.5) | professor: 5, composer: 4, unparsed: 2 |
| yoga_teacher | female | 92.9 (78/84; 85.3–96.7) | 0.3 (6/1759; 0.2–0.7) | 92.9 (78/84; 85.3–96.7) | personal_trainer: 5, comedian: 1 |
| yoga_teacher | male | 87.5 (14/16; 64.0–96.5) | 0.1 (3/2139; 0.0–0.4) | 82.4 (14/17; 59.0–93.8) | software_engineer: 1, physician: 1 |

## GPT-generated-data-GPT-filtering-full__4_original_content_explanation

| Occupation | Gender | TPR | FPR | Precision | Top three error destinations |
|---|---|---|---|---|---|
| accountant | female | 67.6 (25/37; 51.5–80.4) | 0.6 (10/1806; 0.3–1.0) | 71.4 (25/35; 54.9–83.7) | paralegal: 3, journalist: 2, model: 2 |
| accountant | male | 74.6 (47/63; 62.7–83.7) | 0.4 (9/2092; 0.2–0.8) | 83.9 (47/56; 72.2–91.3) | journalist: 4, attorney: 4, model: 2 |
| architect | female | 62.5 (15/24; 42.7–78.8) | 0.2 (3/1819; 0.1–0.5) | 83.3 (15/18; 60.8–94.2) | interior_designer: 6, software_engineer: 1, nurse: 1 |
| architect | male | 64.1 (50/78; 53.0–73.9) | 0.5 (11/2077; 0.3–0.9) | 82.0 (50/61; 70.5–89.6) | software_engineer: 9, interior_designer: 6, professor: 5 |
| attorney | female | 87.0 (67/77; 77.7–92.8) | 0.7 (13/1766; 0.4–1.3) | 83.8 (67/80; 74.2–90.3) | paralegal: 3, accountant: 2, professor: 1 |
| attorney | male | 90.4 (113/125; 84.0–94.4) | 0.6 (12/2030; 0.3–1.0) | 90.4 (113/125; 84.0–94.4) | professor: 4, accountant: 3, journalist: 1 |
| chiropractor | female | 88.5 (23/26; 71.0–96.0) | 1.0 (19/1817; 0.7–1.6) | 54.8 (23/42; 39.9–68.8) | teacher: 1, personal_trainer: 1, dentist: 1 |
| chiropractor | male | 85.1 (63/74; 75.3–91.5) | 1.0 (21/2081; 0.7–1.5) | 75.0 (63/84; 64.8–83.0) | surgeon: 2, dietitian: 2, attorney: 1 |
| comedian | female | 76.2 (16/21; 54.9–89.4) | 0.1 (2/1822; 0.0–0.4) | 88.9 (16/18; 67.2–96.9) | journalist: 3, paralegal: 1, model: 1 |
| comedian | male | 94.9 (75/79; 87.7–98.0) | 0.2 (5/2076; 0.1–0.6) | 93.8 (75/80; 86.2–97.3) | dj: 2, journalist: 1, rapper: 1 |
| composer | female | 87.5 (14/16; 64.0–96.5) | 0.0 (0/1827; 0.0–0.2) | 100.0 (14/14; 78.5–100.0) | comedian: 1, teacher: 1 |
| composer | male | 91.7 (77/84; 83.8–95.9) | 0.4 (8/2071; 0.2–0.8) | 90.6 (77/85; 82.5–95.2) | dj: 2, rapper: 1, architect: 1 |
| dentist | female | 88.2 (45/51; 76.6–94.5) | 0.1 (2/1792; 0.0–0.4) | 95.7 (45/47; 85.8–98.8) | professor: 1, psychologist: 1, physician: 1 |
| dentist | male | 89.5 (85/95; 81.7–94.2) | 0.2 (4/2060; 0.1–0.5) | 95.5 (85/89; 89.0–98.2) | chiropractor: 4, surgeon: 2, professor: 2 |
| dietitian | female | 93.5 (87/93; 86.6–97.0) | 0.5 (9/1750; 0.3–1.0) | 90.6 (87/96; 83.1–95.0) | professor: 3, teacher: 1, chiropractor: 1 |
| dietitian | male | 85.7 (6/7; 48.7–97.4) | 0.1 (2/2148; 0.0–0.3) | 75.0 (6/8; 40.9–92.9) | physician: 1 |
| dj | female | 85.7 (12/14; 60.1–96.0) | 0.1 (1/1829; 0.0–0.3) | 92.3 (12/13; 66.7–98.6) | model: 1, accountant: 1 |
| dj | male | 87.2 (75/86; 78.5–92.7) | 0.5 (10/2069; 0.3–0.9) | 88.2 (75/85; 79.7–93.5) | rapper: 3, comedian: 2, personal_trainer: 1 |
| filmmaker | female | 81.8 (27/33; 65.6–91.4) | 0.0 (0/1810; 0.0–0.2) | 100.0 (27/27; 87.5–100.0) | psychologist: 2, professor: 1, photographer: 1 |
| filmmaker | male | 86.6 (58/67; 76.4–92.8) | 0.1 (2/2088; 0.0–0.3) | 96.7 (58/60; 88.6–99.1) | photographer: 2, journalist: 2, professor: 2 |
| interior_designer | female | 87.7 (71/81; 78.7–93.2) | 0.6 (10/1762; 0.3–1.0) | 87.7 (71/81; 78.7–93.2) | model: 4, accountant: 1, architect: 1 |
| interior_designer | male | 84.2 (16/19; 62.4–94.5) | 0.3 (6/2136; 0.1–0.6) | 72.7 (16/22; 51.8–86.8) | architect: 2, attorney: 1 |
| journalist | female | 83.8 (83/99; 75.3–89.8) | 0.9 (15/1744; 0.5–1.4) | 84.7 (83/98; 76.3–90.5) | model: 3, photographer: 2, professor: 2 |
| journalist | male | 85.3 (87/102; 77.1–90.9) | 1.0 (21/2053; 0.7–1.6) | 80.6 (87/108; 72.1–86.9) | professor: 5, photographer: 2, poet: 2 |
| model | female | 88.0 (73/83; 79.2–93.3) | 0.9 (16/1760; 0.6–1.5) | 82.0 (73/89; 72.8–88.6) | journalist: 2, personal_trainer: 1, rapper: 1 |
| model | male | 82.4 (14/17; 59.0–93.8) | 0.4 (8/2138; 0.2–0.7) | 63.6 (14/22; 43.0–80.3) | professor: 1, unparsed: 1, attorney: 1 |
| nurse | female | 82.8 (144/174; 76.5–87.6) | 1.0 (17/1669; 0.6–1.6) | 89.4 (144/161; 83.7–93.3) | chiropractor: 9, professor: 7, teacher: 3 |
| nurse | male | 70.6 (12/17; 46.9–86.7) | 0.0 (0/2138; -0.0–0.2) | 100.0 (12/12; 75.8–100.0) | chiropractor: 2, psychologist: 1, physician: 1 |
| painter | female | 91.3 (42/46; 79.7–96.6) | 0.3 (5/1797; 0.1–0.6) | 89.4 (42/47; 77.4–95.4) | photographer: 3, poet: 1 |
| painter | male | 90.7 (49/54; 80.1–96.0) | 0.3 (6/2101; 0.1–0.6) | 89.1 (49/55; 78.2–94.9) | unparsed: 2, photographer: 2, software_engineer: 1 |
| paralegal | female | 84.7 (72/85; 75.6–90.8) | 0.6 (10/1758; 0.3–1.0) | 87.8 (72/82; 79.0–93.2) | attorney: 10, photographer: 2, accountant: 1 |
| paralegal | male | 66.7 (10/15; 41.7–84.8) | 0.0 (0/2140; 0.0–0.2) | 100.0 (10/10; 72.2–100.0) | attorney: 2, software_engineer: 1, unparsed: 1 |
| pastor | female | 95.8 (23/24; 79.8–99.3) | 0.5 (10/1819; 0.3–1.0) | 69.7 (23/33; 52.7–82.6) | interior_designer: 1 |
| pastor | male | 88.2 (67/76; 79.0–93.6) | 0.6 (13/2079; 0.4–1.1) | 83.8 (67/80; 74.2–90.3) | teacher: 2, journalist: 2, psychologist: 2 |
| personal_trainer | female | 91.3 (42/46; 79.7–96.6) | 0.2 (3/1797; 0.1–0.5) | 93.3 (42/45; 82.1–97.7) | dietitian: 2, pastor: 1, model: 1 |
| personal_trainer | male | 90.6 (48/53; 79.7–95.9) | 0.2 (4/2102; 0.1–0.5) | 92.3 (48/52; 81.8–97.0) | chiropractor: 2, model: 2, teacher: 1 |
| photographer | female | 91.5 (65/71; 82.8–96.1) | 0.7 (13/1772; 0.4–1.3) | 83.3 (65/78; 73.5–90.0) | nurse: 2, architect: 1, dietitian: 1 |
| photographer | male | 93.0 (120/129; 87.3–96.3) | 0.5 (11/2026; 0.3–1.0) | 91.6 (120/131; 85.6–95.2) | teacher: 3, journalist: 2, poet: 1 |
| physician | female | 79.1 (117/148; 71.8–84.8) | 0.3 (5/1695; 0.1–0.7) | 95.9 (117/122; 90.8–98.2) | surgeon: 12, chiropractor: 8, nurse: 6 |
| physician | male | 64.5 (98/152; 56.6–71.6) | 0.6 (13/2003; 0.4–1.1) | 88.3 (98/111; 81.0–93.0) | surgeon: 24, professor: 15, chiropractor: 11 |
| poet | female | 91.8 (45/49; 80.8–96.8) | 0.4 (7/1794; 0.2–0.8) | 86.5 (45/52; 74.7–93.3) | painter: 1, dietitian: 1, professor: 1 |
| poet | male | 80.4 (41/51; 67.5–89.0) | 0.5 (11/2104; 0.3–0.9) | 78.8 (41/52; 66.0–87.8) | journalist: 3, rapper: 3, professor: 2 |
| professor | female | 93.4 (253/271; 89.7–95.8) | 2.4 (37/1572; 1.7–3.2) | 87.2 (253/290; 82.9–90.6) | teacher: 6, psychologist: 4, journalist: 2 |
| professor | male | 91.5 (301/329; 88.0–94.0) | 3.2 (59/1826; 2.5–4.1) | 83.6 (301/360; 79.4–87.1) | surgeon: 4, attorney: 3, software_engineer: 3 |
| psychologist | female | 78.1 (50/64; 66.6–86.5) | 0.6 (10/1779; 0.3–1.0) | 83.3 (50/60; 72.0–90.7) | professor: 8, nurse: 2, attorney: 1 |
| psychologist | male | 79.5 (31/39; 64.5–89.2) | 0.4 (9/2116; 0.2–0.8) | 77.5 (31/40; 62.5–87.7) | teacher: 2, professor: 2, personal_trainer: 1 |
| rapper | female | 90.0 (9/10; 59.6–98.2) | 0.1 (1/1833; 0.0–0.3) | 90.0 (9/10; 59.6–98.2) | painter: 1 |
| rapper | male | 93.3 (84/90; 86.2–96.9) | 0.4 (9/2065; 0.2–0.8) | 90.3 (84/93; 82.6–94.8) | dj: 4, poet: 2 |
| software_engineer | female | 87.5 (14/16; 64.0–96.5) | 0.1 (2/1827; 0.0–0.4) | 87.5 (14/16; 64.0–96.5) | professor: 1, architect: 1 |
| software_engineer | male | 82.1 (69/84; 72.6–88.9) | 0.8 (16/2071; 0.5–1.3) | 81.2 (69/85; 71.6–88.1) | architect: 5, professor: 5, accountant: 1 |
| surgeon | female | 64.7 (11/17; 41.3–82.7) | 0.8 (15/1826; 0.5–1.4) | 42.3 (11/26; 25.5–61.1) | professor: 2, dentist: 1, physician: 1 |
| surgeon | male | 83.8 (83/99; 75.3–89.8) | 1.6 (32/2056; 1.1–2.2) | 72.2 (83/115; 63.4–79.5) | professor: 5, physician: 4, dentist: 3 |
| teacher | female | 66.3 (55/83; 55.6–75.5) | 1.0 (17/1760; 0.6–1.5) | 76.4 (55/72; 65.4–84.7) | pastor: 6, yoga_teacher: 6, professor: 4 |
| teacher | male | 65.5 (36/55; 52.3–76.6) | 0.7 (15/2100; 0.4–1.2) | 70.6 (36/51; 57.0–81.3) | professor: 7, composer: 2, pastor: 2 |
| yoga_teacher | female | 97.6 (82/84; 91.7–99.3) | 0.3 (6/1759; 0.2–0.7) | 93.2 (82/88; 85.9–96.8) | personal_trainer: 1, comedian: 1 |
| yoga_teacher | male | 81.2 (13/16; 57.0–93.4) | 0.1 (2/2139; 0.0–0.3) | 86.7 (13/15; 62.1–96.3) | accountant: 1, poet: 1, physician: 1 |

## GPT-generated-data-GPT-filtering-full__5_original_random

| Occupation | Gender | TPR | FPR | Precision | Top three error destinations |
|---|---|---|---|---|---|
| accountant | female | 73.0 (27/37; 57.0–84.6) | 0.7 (12/1806; 0.4–1.2) | 69.2 (27/39; 53.6–81.4) | nurse: 3, model: 2, paralegal: 2 |
| accountant | male | 76.2 (48/63; 64.4–85.0) | 0.4 (9/2092; 0.2–0.8) | 84.2 (48/57; 72.6–91.5) | attorney: 4, journalist: 3, architect: 2 |
| architect | female | 70.8 (17/24; 50.8–85.1) | 0.4 (7/1819; 0.2–0.8) | 70.8 (17/24; 50.8–85.1) | interior_designer: 4, software_engineer: 1, professor: 1 |
| architect | male | 71.8 (56/78; 61.0–80.6) | 1.0 (21/2077; 0.7–1.5) | 72.7 (56/77; 61.9–81.4) | software_engineer: 8, interior_designer: 4, professor: 3 |
| attorney | female | 88.3 (68/77; 79.3–93.7) | 0.9 (16/1766; 0.6–1.5) | 81.0 (68/84; 71.3–87.9) | nurse: 2, paralegal: 2, accountant: 2 |
| attorney | male | 92.0 (115/125; 85.9–95.6) | 0.7 (15/2030; 0.4–1.2) | 88.5 (115/130; 81.8–92.9) | accountant: 5, journalist: 1, composer: 1 |
| chiropractor | female | 69.2 (18/26; 50.0–83.5) | 0.3 (5/1817; 0.1–0.6) | 78.3 (18/23; 58.1–90.3) | nurse: 4, personal_trainer: 2, physician: 2 |
| chiropractor | male | 83.8 (62/74; 73.8–90.5) | 0.8 (17/2081; 0.5–1.3) | 78.5 (62/79; 68.2–86.1) | physician: 3, personal_trainer: 2, attorney: 1 |
| comedian | female | 81.0 (17/21; 60.0–92.3) | 0.1 (2/1822; 0.0–0.4) | 89.5 (17/19; 68.6–97.1) | nurse: 2, personal_trainer: 1, model: 1 |
| comedian | male | 96.2 (76/79; 89.4–98.7) | 0.3 (6/2076; 0.1–0.6) | 92.7 (76/82; 84.9–96.6) | dj: 1, attorney: 1, rapper: 1 |
| composer | female | 81.2 (13/16; 57.0–93.4) | 0.0 (0/1827; 0.0–0.2) | 100.0 (13/13; 77.2–100.0) | comedian: 1, professor: 1, teacher: 1 |
| composer | male | 96.4 (81/84; 90.0–98.8) | 0.5 (10/2071; 0.3–0.9) | 89.0 (81/91; 80.9–93.9) | architect: 1, teacher: 1, rapper: 1 |
| dentist | female | 90.2 (46/51; 79.0–95.7) | 0.1 (1/1792; 0.0–0.3) | 97.9 (46/47; 88.9–99.6) | professor: 1, physician: 1, nurse: 1 |
| dentist | male | 90.5 (86/95; 83.0–94.9) | 0.2 (4/2060; 0.1–0.5) | 95.6 (86/90; 89.1–98.3) | chiropractor: 5, photographer: 1, physician: 1 |
| dietitian | female | 92.5 (86/93; 85.3–96.3) | 0.5 (8/1750; 0.2–0.9) | 91.5 (86/94; 84.1–95.6) | nurse: 2, personal_trainer: 1, physician: 1 |
| dietitian | male | 85.7 (6/7; 48.7–97.4) | 0.0 (1/2148; 0.0–0.3) | 85.7 (6/7; 48.7–97.4) | physician: 1 |
| dj | female | 85.7 (12/14; 60.1–96.0) | 0.0 (0/1829; 0.0–0.2) | 100.0 (12/12; 75.8–100.0) | model: 1, poet: 1 |
| dj | male | 88.4 (76/86; 79.9–93.6) | 0.3 (7/2069; 0.2–0.7) | 91.6 (76/83; 83.6–95.9) | rapper: 2, comedian: 2, personal_trainer: 1 |
| filmmaker | female | 84.8 (28/33; 69.1–93.3) | 0.1 (2/1810; 0.0–0.4) | 93.3 (28/30; 78.7–98.2) | psychologist: 2, professor: 1, photographer: 1 |
| filmmaker | male | 91.0 (61/67; 81.8–95.8) | 0.2 (5/2088; 0.1–0.6) | 92.4 (61/66; 83.5–96.7) | photographer: 2, journalist: 2, poet: 1 |
| interior_designer | female | 85.2 (69/81; 75.9–91.3) | 0.6 (11/1762; 0.3–1.1) | 86.2 (69/80; 77.0–92.1) | model: 5, architect: 3, accountant: 2 |
| interior_designer | male | 84.2 (16/19; 62.4–94.5) | 0.3 (6/2136; 0.1–0.6) | 72.7 (16/22; 51.8–86.8) | architect: 2, attorney: 1 |
| journalist | female | 81.8 (81/99; 73.1–88.2) | 0.3 (6/1744; 0.2–0.7) | 93.1 (81/87; 85.8–96.8) | model: 4, teacher: 2, professor: 2 |
| journalist | male | 89.2 (91/102; 81.7–93.9) | 0.9 (18/2053; 0.6–1.4) | 83.5 (91/109; 75.4–89.3) | professor: 4, poet: 2, psychologist: 1 |
| model | female | 91.6 (76/83; 83.6–95.9) | 1.1 (19/1760; 0.7–1.7) | 80.0 (76/95; 70.9–86.8) | personal_trainer: 1, nurse: 1, journalist: 1 |
| model | male | 82.4 (14/17; 59.0–93.8) | 0.3 (7/2138; 0.2–0.7) | 66.7 (14/21; 45.4–82.8) | professor: 2, attorney: 1 |
| nurse | female | 90.8 (158/174; 85.6–94.3) | 3.0 (50/1669; 2.3–3.9) | 76.0 (158/208; 69.7–81.3) | chiropractor: 2, accountant: 2, dietitian: 2 |
| nurse | male | 70.6 (12/17; 46.9–86.7) | 0.5 (10/2138; 0.3–0.9) | 54.5 (12/22; 34.7–73.1) | chiropractor: 3, psychologist: 1, professor: 1 |
| painter | female | 82.6 (38/46; 69.3–90.9) | 0.2 (4/1797; 0.1–0.6) | 90.5 (38/42; 77.9–96.2) | photographer: 5, unparsed: 1, poet: 1 |
| painter | male | 83.3 (45/54; 71.3–91.0) | 0.2 (4/2101; 0.1–0.5) | 91.8 (45/49; 80.8–96.8) | photographer: 5, unparsed: 2, software_engineer: 1 |
| paralegal | female | 84.7 (72/85; 75.6–90.8) | 0.3 (6/1758; 0.2–0.7) | 92.3 (72/78; 84.2–96.4) | attorney: 11, interior_designer: 1, photographer: 1 |
| paralegal | male | 66.7 (10/15; 41.7–84.8) | 0.0 (0/2140; 0.0–0.2) | 100.0 (10/10; 72.2–100.0) | attorney: 4, accountant: 1 |
| pastor | female | 79.2 (19/24; 59.5–90.8) | 0.3 (6/1819; 0.2–0.7) | 76.0 (19/25; 56.6–88.5) | nurse: 2, teacher: 1, model: 1 |
| pastor | male | 85.5 (65/76; 75.9–91.7) | 0.5 (10/2079; 0.3–0.9) | 86.7 (65/75; 77.2–92.6) | accountant: 2, comedian: 2, painter: 1 |
| personal_trainer | female | 95.7 (44/46; 85.5–98.8) | 0.6 (10/1797; 0.3–1.0) | 81.5 (44/54; 69.2–89.6) | nurse: 1, pastor: 1 |
| personal_trainer | male | 94.3 (50/53; 84.6–98.1) | 0.3 (6/2102; 0.1–0.6) | 89.3 (50/56; 78.5–95.0) | model: 2, nurse: 1 |
| photographer | female | 93.0 (66/71; 84.6–97.0) | 0.8 (14/1772; 0.5–1.3) | 82.5 (66/80; 72.7–89.3) | architect: 1, dietitian: 1, model: 1 |
| photographer | male | 93.8 (121/129; 88.2–96.8) | 0.8 (16/2026; 0.5–1.3) | 88.3 (121/137; 81.9–92.7) | journalist: 2, poet: 1, interior_designer: 1 |
| physician | female | 83.1 (123/148; 76.3–88.3) | 0.7 (12/1695; 0.4–1.2) | 91.1 (123/135; 85.1–94.8) | nurse: 14, surgeon: 8, professor: 2 |
| physician | male | 74.3 (113/152; 66.9–80.6) | 0.9 (18/2003; 0.6–1.4) | 86.3 (113/131; 79.3–91.1) | surgeon: 16, professor: 8, chiropractor: 7 |
| poet | female | 91.8 (45/49; 80.8–96.8) | 0.7 (12/1794; 0.4–1.2) | 78.9 (45/57; 66.7–87.5) | painter: 1, dietitian: 1, model: 1 |
| poet | male | 76.5 (39/51; 63.2–86.0) | 0.6 (12/2104; 0.3–1.0) | 76.5 (39/51; 63.2–86.0) | rapper: 4, photographer: 2, journalist: 2 |
| professor | female | 90.8 (246/271; 86.7–93.7) | 1.5 (23/1572; 1.0–2.2) | 91.4 (246/269; 87.5–94.2) | teacher: 5, psychologist: 4, dietitian: 2 |
| professor | male | 88.8 (292/329; 84.9–91.7) | 1.9 (35/1826; 1.4–2.7) | 89.3 (292/327; 85.5–92.2) | surgeon: 7, journalist: 3, attorney: 3 |
| psychologist | female | 67.2 (43/64; 55.0–77.4) | 0.5 (9/1779; 0.3–1.0) | 82.7 (43/52; 70.3–90.6) | professor: 7, nurse: 4, teacher: 2 |
| psychologist | male | 79.5 (31/39; 64.5–89.2) | 0.5 (11/2116; 0.3–0.9) | 73.8 (31/42; 58.9–84.7) | professor: 2, personal_trainer: 1, teacher: 1 |
| rapper | female | 90.0 (9/10; 59.6–98.2) | 0.0 (0/1833; 0.0–0.2) | 100.0 (9/9; 70.1–100.0) | painter: 1 |
| rapper | male | 92.2 (83/90; 84.8–96.2) | 0.4 (8/2065; 0.2–0.8) | 91.2 (83/91; 83.6–95.5) | dj: 4, poet: 2, model: 1 |
| software_engineer | female | 81.2 (13/16; 57.0–93.4) | 0.1 (1/1827; 0.0–0.3) | 92.9 (13/14; 68.5–98.7) | architect: 2, professor: 1 |
| software_engineer | male | 77.4 (65/84; 67.4–85.0) | 0.6 (13/2071; 0.4–1.1) | 83.3 (65/78; 73.5–90.0) | architect: 8, journalist: 2, psychologist: 1 |
| surgeon | female | 76.5 (13/17; 52.7–90.4) | 0.7 (12/1826; 0.4–1.1) | 52.0 (13/25; 33.5–70.0) | dentist: 1, physician: 1, model: 1 |
| surgeon | male | 84.8 (84/99; 76.5–90.6) | 1.2 (24/2056; 0.8–1.7) | 77.8 (84/108; 69.1–84.6) | physician: 7, dentist: 3, nurse: 2 |
| teacher | female | 55.4 (46/83; 44.7–65.6) | 0.9 (15/1760; 0.5–1.4) | 75.4 (46/61; 63.3–84.5) | nurse: 6, yoga_teacher: 4, professor: 4 |
| teacher | male | 63.6 (35/55; 50.4–75.1) | 0.3 (6/2100; 0.1–0.6) | 85.4 (35/41; 71.6–93.1) | professor: 6, composer: 2, unparsed: 2 |
| yoga_teacher | female | 90.5 (76/84; 82.3–95.1) | 0.2 (4/1759; 0.1–0.6) | 95.0 (76/80; 87.8–98.0) | personal_trainer: 4, nurse: 3, comedian: 1 |
| yoga_teacher | male | 81.2 (13/16; 57.0–93.4) | 0.1 (2/2139; 0.0–0.3) | 86.7 (13/15; 62.1–96.3) | poet: 2, physician: 1 |

## GPT-generated-data-llama-filtering-full__3_original_content_only

| Occupation | Gender | TPR | FPR | Precision | Top three error destinations |
|---|---|---|---|---|---|
| accountant | female | 67.6 (25/37; 51.5–80.4) | 0.7 (12/1806; 0.4–1.2) | 67.6 (25/37; 51.5–80.4) | journalist: 3, physician: 2, unparsed: 2 |
| accountant | male | 74.6 (47/63; 62.7–83.7) | 0.4 (9/2092; 0.2–0.8) | 83.9 (47/56; 72.2–91.3) | journalist: 3, attorney: 3, architect: 3 |
| architect | female | 62.5 (15/24; 42.7–78.8) | 0.3 (5/1819; 0.1–0.6) | 75.0 (15/20; 53.1–88.8) | interior_designer: 5, software_engineer: 2, nurse: 1 |
| architect | male | 70.5 (55/78; 59.6–79.5) | 0.6 (12/2077; 0.3–1.0) | 82.1 (55/67; 71.3–89.4) | software_engineer: 8, interior_designer: 6, professor: 4 |
| attorney | female | 88.3 (68/77; 79.3–93.7) | 1.0 (17/1766; 0.6–1.5) | 80.0 (68/85; 70.3–87.1) | unparsed: 2, accountant: 2, professor: 1 |
| attorney | male | 90.4 (113/125; 84.0–94.4) | 0.6 (12/2030; 0.3–1.0) | 90.4 (113/125; 84.0–94.4) | accountant: 3, journalist: 2, composer: 1 |
| chiropractor | female | 69.2 (18/26; 50.0–83.5) | 0.2 (3/1817; 0.1–0.5) | 85.7 (18/21; 65.4–95.0) | nurse: 4, teacher: 1, dentist: 1 |
| chiropractor | male | 82.4 (61/74; 72.2–89.4) | 0.7 (15/2081; 0.4–1.2) | 80.3 (61/76; 70.0–87.7) | physician: 4, surgeon: 3, dentist: 1 |
| comedian | female | 76.2 (16/21; 54.9–89.4) | 0.1 (2/1822; 0.0–0.4) | 88.9 (16/18; 67.2–96.9) | nurse: 2, journalist: 2, model: 1 |
| comedian | male | 96.2 (76/79; 89.4–98.7) | 0.0 (0/2076; 0.0–0.2) | 100.0 (76/76; 95.2–100.0) | dj: 1, psychologist: 1, rapper: 1 |
| composer | female | 87.5 (14/16; 64.0–96.5) | 0.1 (2/1827; 0.0–0.4) | 87.5 (14/16; 64.0–96.5) | comedian: 1, teacher: 1 |
| composer | male | 95.2 (80/84; 88.4–98.1) | 0.6 (13/2071; 0.4–1.1) | 86.0 (80/93; 77.5–91.6) | rapper: 1, architect: 1, journalist: 1 |
| dentist | female | 86.3 (44/51; 74.3–93.2) | 0.2 (3/1792; 0.1–0.5) | 93.6 (44/47; 82.8–97.8) | physician: 3, surgeon: 2, nurse: 1 |
| dentist | male | 87.4 (83/95; 79.2–92.6) | 0.2 (4/2060; 0.1–0.5) | 95.4 (83/87; 88.8–98.2) | chiropractor: 4, surgeon: 3, professor: 2 |
| dietitian | female | 92.5 (86/93; 85.3–96.3) | 0.3 (6/1750; 0.2–0.7) | 93.5 (86/92; 86.5–97.0) | nurse: 4, professor: 1, chiropractor: 1 |
| dietitian | male | 71.4 (5/7; 35.9–91.8) | 0.0 (1/2148; 0.0–0.3) | 83.3 (5/6; 43.6–97.0) | personal_trainer: 1, physician: 1 |
| dj | female | 85.7 (12/14; 60.1–96.0) | 0.1 (2/1829; 0.0–0.4) | 85.7 (12/14; 60.1–96.0) | model: 1, software_engineer: 1 |
| dj | male | 88.4 (76/86; 79.9–93.6) | 0.4 (8/2069; 0.2–0.8) | 90.5 (76/84; 82.3–95.1) | rapper: 2, personal_trainer: 1, poet: 1 |
| filmmaker | female | 84.8 (28/33; 69.1–93.3) | 0.1 (1/1810; 0.0–0.3) | 96.6 (28/29; 82.8–99.4) | professor: 1, composer: 1, psychologist: 1 |
| filmmaker | male | 91.0 (61/67; 81.8–95.8) | 0.1 (2/2088; 0.0–0.3) | 96.8 (61/63; 89.1–99.1) | journalist: 2, painter: 1, photographer: 1 |
| interior_designer | female | 88.9 (72/81; 80.2–94.0) | 0.7 (12/1762; 0.4–1.2) | 85.7 (72/84; 76.7–91.6) | model: 4, journalist: 2, accountant: 1 |
| interior_designer | male | 89.5 (17/19; 68.6–97.1) | 0.4 (8/2136; 0.2–0.7) | 68.0 (17/25; 48.4–82.8) | attorney: 1, architect: 1 |
| journalist | female | 84.8 (84/99; 76.5–90.6) | 1.1 (19/1744; 0.7–1.7) | 81.6 (84/103; 73.0–87.9) | unparsed: 3, photographer: 2, model: 2 |
| journalist | male | 91.2 (93/102; 84.1–95.3) | 1.4 (28/2053; 0.9–2.0) | 76.9 (93/121; 68.6–83.5) | professor: 5, software_engineer: 1, psychologist: 1 |
| model | female | 89.2 (74/83; 80.7–94.2) | 0.8 (14/1760; 0.5–1.3) | 84.1 (74/88; 75.0–90.3) | journalist: 2, yoga_teacher: 1, nurse: 1 |
| model | male | 70.6 (12/17; 46.9–86.7) | 0.3 (6/2138; 0.1–0.6) | 66.7 (12/18; 43.7–83.7) | professor: 2, unparsed: 1, rapper: 1 |
| nurse | female | 93.7 (163/174; 89.0–96.4) | 2.7 (45/1669; 2.0–3.6) | 78.4 (163/208; 72.3–83.4) | dietitian: 3, professor: 3, accountant: 1 |
| nurse | male | 70.6 (12/17; 46.9–86.7) | 0.2 (4/2138; 0.1–0.5) | 75.0 (12/16; 50.5–89.8) | physician: 3, psychologist: 1, chiropractor: 1 |
| painter | female | 89.1 (41/46; 77.0–95.3) | 0.2 (4/1797; 0.1–0.6) | 91.1 (41/45; 79.3–96.5) | photographer: 3, poet: 1, filmmaker: 1 |
| painter | male | 87.0 (47/54; 75.6–93.6) | 0.2 (4/2101; 0.1–0.5) | 92.2 (47/51; 81.5–96.9) | photographer: 5, unparsed: 1, poet: 1 |
| paralegal | female | 77.6 (66/85; 67.7–85.2) | 0.1 (1/1758; 0.0–0.3) | 98.5 (66/67; 92.0–99.7) | attorney: 13, accountant: 1, journalist: 1 |
| paralegal | male | 60.0 (9/15; 35.7–80.2) | 0.0 (0/2140; 0.0–0.2) | 100.0 (9/9; 70.1–100.0) | attorney: 4, software_engineer: 1, unparsed: 1 |
| pastor | female | 87.5 (21/24; 69.0–95.7) | 0.4 (7/1819; 0.2–0.8) | 75.0 (21/28; 56.6–87.3) | nurse: 2, interior_designer: 1 |
| pastor | male | 84.2 (64/76; 74.4–90.7) | 0.5 (10/2079; 0.3–0.9) | 86.5 (64/74; 76.9–92.5) | journalist: 2, teacher: 2, photographer: 1 |
| personal_trainer | female | 93.5 (43/46; 82.5–97.8) | 0.1 (2/1797; 0.0–0.4) | 95.6 (43/45; 85.2–98.8) | pastor: 1, teacher: 1, dietitian: 1 |
| personal_trainer | male | 92.5 (49/53; 82.1–97.0) | 0.1 (3/2102; 0.0–0.4) | 94.2 (49/52; 84.4–98.0) | model: 2, nurse: 1, surgeon: 1 |
| photographer | female | 93.0 (66/71; 84.6–97.0) | 0.5 (9/1772; 0.3–1.0) | 88.0 (66/75; 78.7–93.6) | architect: 1, dietitian: 1, model: 1 |
| photographer | male | 94.6 (122/129; 89.2–97.3) | 0.7 (15/2026; 0.4–1.2) | 89.1 (122/137; 82.7–93.3) | journalist: 3, accountant: 1, interior_designer: 1 |
| physician | female | 81.8 (121/148; 74.8–87.1) | 0.5 (8/1695; 0.2–0.9) | 93.8 (121/129; 88.2–96.8) | nurse: 13, surgeon: 7, professor: 5 |
| physician | male | 65.1 (99/152; 57.3–72.2) | 1.1 (23/2003; 0.8–1.7) | 81.1 (99/122; 73.3–87.1) | surgeon: 30, professor: 10, chiropractor: 8 |
| poet | female | 85.7 (42/49; 73.3–92.9) | 0.6 (10/1794; 0.3–1.0) | 80.8 (42/52; 68.1–89.2) | comedian: 1, painter: 1, yoga_teacher: 1 |
| poet | male | 76.5 (39/51; 63.2–86.0) | 0.3 (6/2104; 0.1–0.6) | 86.7 (39/45; 73.8–93.7) | journalist: 4, rapper: 4, professor: 2 |
| professor | female | 91.5 (248/271; 87.6–94.3) | 1.8 (28/1572; 1.2–2.6) | 89.9 (248/276; 85.7–92.9) | teacher: 5, poet: 3, journalist: 3 |
| professor | male | 89.7 (295/329; 85.9–92.5) | 2.3 (42/1826; 1.7–3.1) | 87.5 (295/337; 83.6–90.6) | surgeon: 7, physician: 4, composer: 4 |
| psychologist | female | 75.0 (48/64; 63.2–84.0) | 0.3 (6/1779; 0.2–0.7) | 88.9 (48/54; 77.8–94.8) | professor: 9, nurse: 3, interior_designer: 1 |
| psychologist | male | 76.9 (30/39; 61.7–87.4) | 0.5 (10/2116; 0.3–0.9) | 75.0 (30/40; 59.8–85.8) | professor: 3, journalist: 2, teacher: 2 |
| rapper | female | 80.0 (8/10; 49.0–94.3) | 0.0 (0/1833; 0.0–0.2) | 100.0 (8/8; 67.6–100.0) | model: 1, painter: 1 |
| rapper | male | 91.1 (82/90; 83.4–95.4) | 0.4 (9/2065; 0.2–0.8) | 90.1 (82/91; 82.3–94.7) | dj: 5, poet: 2, model: 1 |
| software_engineer | female | 81.2 (13/16; 57.0–93.4) | 0.2 (4/1827; 0.1–0.6) | 76.5 (13/17; 52.7–90.4) | architect: 2, professor: 1 |
| software_engineer | male | 82.1 (69/84; 72.6–88.9) | 0.7 (15/2071; 0.4–1.2) | 82.1 (69/84; 72.6–88.9) | professor: 4, architect: 3, composer: 2 |
| surgeon | female | 76.5 (13/17; 52.7–90.4) | 0.6 (11/1826; 0.3–1.1) | 54.2 (13/24; 35.1–72.1) | dentist: 1, physician: 1, nurse: 1 |
| surgeon | male | 86.9 (86/99; 78.8–92.2) | 2.1 (44/2056; 1.6–2.9) | 66.2 (86/130; 57.7–73.7) | physician: 5, dentist: 3, nurse: 2 |
| teacher | female | 56.6 (47/83; 45.9–66.8) | 0.7 (13/1760; 0.4–1.3) | 78.3 (47/60; 66.4–86.9) | accountant: 6, yoga_teacher: 5, nurse: 4 |
| teacher | male | 65.5 (36/55; 52.3–76.6) | 0.3 (7/2100; 0.2–0.7) | 83.7 (36/43; 70.0–91.9) | professor: 4, composer: 3, journalist: 2 |
| yoga_teacher | female | 96.4 (81/84; 90.0–98.8) | 0.5 (8/1759; 0.2–0.9) | 91.0 (81/89; 83.3–95.4) | personal_trainer: 1, dj: 1, nurse: 1 |
| yoga_teacher | male | 81.2 (13/16; 57.0–93.4) | 0.1 (2/2139; 0.0–0.3) | 86.7 (13/15; 62.1–96.3) | software_engineer: 1, poet: 1, physician: 1 |

## GPT-generated-data-llama-filtering-full__4_original_content_explanation

| Occupation | Gender | TPR | FPR | Precision | Top three error destinations |
|---|---|---|---|---|---|
| accountant | female | 70.3 (26/37; 54.2–82.5) | 0.3 (6/1806; 0.2–0.7) | 81.2 (26/32; 64.7–91.1) | paralegal: 4, journalist: 2, physician: 2 |
| accountant | male | 68.3 (43/63; 56.0–78.4) | 0.3 (6/2092; 0.1–0.6) | 87.8 (43/49; 75.8–94.3) | journalist: 5, attorney: 4, pastor: 3 |
| architect | female | 66.7 (16/24; 46.7–82.0) | 0.2 (4/1819; 0.1–0.6) | 80.0 (16/20; 58.4–91.9) | interior_designer: 4, software_engineer: 1, dj: 1 |
| architect | male | 61.5 (48/78; 50.4–71.6) | 0.4 (8/2077; 0.2–0.8) | 85.7 (48/56; 74.3–92.6) | software_engineer: 14, professor: 5, interior_designer: 4 |
| attorney | female | 77.9 (60/77; 67.5–85.7) | 0.5 (8/1766; 0.2–0.9) | 88.2 (60/68; 78.5–93.9) | paralegal: 9, professor: 2, unparsed: 1 |
| attorney | male | 88.0 (110/125; 81.1–92.6) | 0.6 (13/2030; 0.4–1.1) | 89.4 (110/123; 82.8–93.7) | journalist: 5, paralegal: 5, comedian: 1 |
| chiropractor | female | 80.8 (21/26; 62.1–91.5) | 0.7 (13/1817; 0.4–1.2) | 61.8 (21/34; 45.0–76.1) | physician: 2, teacher: 1, dentist: 1 |
| chiropractor | male | 87.8 (65/74; 78.5–93.5) | 1.1 (23/2081; 0.7–1.7) | 73.9 (65/88; 63.8–81.9) | physician: 3, pastor: 1, personal_trainer: 1 |
| comedian | female | 81.0 (17/21; 60.0–92.3) | 0.2 (3/1822; 0.1–0.5) | 85.0 (17/20; 64.0–94.8) | journalist: 2, dj: 1, unparsed: 1 |
| comedian | male | 96.2 (76/79; 89.4–98.7) | 0.4 (9/2076; 0.2–0.8) | 89.4 (76/85; 81.1–94.3) | dj: 1, journalist: 1, rapper: 1 |
| composer | female | 87.5 (14/16; 64.0–96.5) | 0.1 (1/1827; 0.0–0.3) | 93.3 (14/15; 70.2–98.8) | comedian: 1, teacher: 1 |
| composer | male | 95.2 (80/84; 88.4–98.1) | 0.2 (5/2071; 0.1–0.6) | 94.1 (80/85; 87.0–97.5) | rapper: 1, architect: 1, teacher: 1 |
| dentist | female | 90.2 (46/51; 79.0–95.7) | 0.2 (3/1792; 0.1–0.5) | 93.9 (46/49; 83.5–97.9) | surgeon: 2, physician: 1, nurse: 1 |
| dentist | male | 88.4 (84/95; 80.4–93.4) | 0.1 (3/2060; 0.0–0.4) | 96.6 (84/87; 90.3–98.8) | chiropractor: 5, professor: 2, photographer: 1 |
| dietitian | female | 88.2 (82/93; 80.1–93.3) | 0.1 (2/1750; 0.0–0.4) | 97.6 (82/84; 91.7–99.3) | chiropractor: 3, nurse: 2, physician: 1 |
| dietitian | male | 85.7 (6/7; 48.7–97.4) | 0.0 (1/2148; 0.0–0.3) | 85.7 (6/7; 48.7–97.4) | physician: 1 |
| dj | female | 92.9 (13/14; 68.5–98.7) | 0.2 (3/1829; 0.1–0.5) | 81.2 (13/16; 57.0–93.4) | model: 1 |
| dj | male | 90.7 (78/86; 82.7–95.2) | 0.4 (9/2069; 0.2–0.8) | 89.7 (78/87; 81.5–94.5) | rapper: 2, personal_trainer: 1, poet: 1 |
| filmmaker | female | 81.8 (27/33; 65.6–91.4) | 0.1 (1/1810; 0.0–0.3) | 96.4 (27/28; 82.3–99.4) | psychologist: 3, professor: 1, composer: 1 |
| filmmaker | male | 80.6 (54/67; 69.6–88.3) | 0.1 (2/2088; 0.0–0.3) | 96.4 (54/56; 87.9–99.0) | journalist: 8, photographer: 2, painter: 1 |
| interior_designer | female | 86.4 (70/81; 77.3–92.2) | 0.5 (9/1762; 0.3–1.0) | 88.6 (70/79; 79.7–93.9) | model: 3, architect: 2, psychologist: 2 |
| interior_designer | male | 89.5 (17/19; 68.6–97.1) | 0.2 (5/2136; 0.1–0.5) | 77.3 (17/22; 56.6–89.9) | attorney: 1, architect: 1 |
| journalist | female | 84.8 (84/99; 76.5–90.6) | 1.4 (25/1744; 1.0–2.1) | 77.1 (84/109; 68.3–84.0) | model: 2, photographer: 2, nurse: 2 |
| journalist | male | 92.2 (94/102; 85.3–96.0) | 1.8 (37/2053; 1.3–2.5) | 71.8 (94/131; 63.5–78.8) | professor: 3, poet: 1, comedian: 1 |
| model | female | 88.0 (73/83; 79.2–93.3) | 0.6 (10/1760; 0.3–1.0) | 88.0 (73/83; 79.2–93.3) | interior_designer: 2, journalist: 2, personal_trainer: 1 |
| model | male | 70.6 (12/17; 46.9–86.7) | 0.1 (3/2138; 0.0–0.4) | 80.0 (12/15; 54.8–93.0) | teacher: 2, professor: 1, unparsed: 1 |
| nurse | female | 84.5 (147/174; 78.4–89.1) | 1.4 (24/1669; 1.0–2.1) | 86.0 (147/171; 80.0–90.4) | physician: 5, chiropractor: 5, journalist: 5 |
| nurse | male | 76.5 (13/17; 52.7–90.4) | 0.0 (1/2138; 0.0–0.3) | 92.9 (13/14; 68.5–98.7) | chiropractor: 3, psychologist: 1 |
| painter | female | 93.5 (43/46; 82.5–97.8) | 0.5 (9/1797; 0.3–0.9) | 82.7 (43/52; 70.3–90.6) | poet: 1, journalist: 1, photographer: 1 |
| painter | male | 87.0 (47/54; 75.6–93.6) | 0.3 (6/2101; 0.1–0.6) | 88.7 (47/53; 77.4–94.7) | photographer: 4, unparsed: 1, software_engineer: 1 |
| paralegal | female | 90.6 (77/85; 82.5–95.2) | 0.9 (16/1758; 0.6–1.5) | 82.8 (77/93; 73.9–89.1) | attorney: 5, teacher: 1, interior_designer: 1 |
| paralegal | male | 80.0 (12/15; 54.8–93.0) | 0.3 (7/2140; 0.2–0.7) | 63.2 (12/19; 41.0–80.9) | attorney: 2, software_engineer: 1 |
| pastor | female | 95.8 (23/24; 79.8–99.3) | 0.8 (14/1819; 0.5–1.3) | 62.2 (23/37; 46.1–75.9) | interior_designer: 1 |
| pastor | male | 88.2 (67/76; 79.0–93.6) | 0.5 (11/2079; 0.3–0.9) | 85.9 (67/78; 76.5–91.9) | journalist: 3, teacher: 2, comedian: 2 |
| personal_trainer | female | 97.8 (45/46; 88.7–99.6) | 0.2 (3/1797; 0.1–0.5) | 93.8 (45/48; 83.2–97.9) | pastor: 1 |
| personal_trainer | male | 90.6 (48/53; 79.7–95.9) | 0.1 (3/2102; 0.0–0.4) | 94.1 (48/51; 84.1–98.0) | chiropractor: 2, model: 2, teacher: 1 |
| photographer | female | 91.5 (65/71; 82.8–96.1) | 0.4 (7/1772; 0.2–0.8) | 90.3 (65/72; 81.3–95.2) | painter: 3, dietitian: 1, model: 1 |
| photographer | male | 93.8 (121/129; 88.2–96.8) | 0.6 (13/2026; 0.4–1.1) | 90.3 (121/134; 84.1–94.2) | journalist: 2, attorney: 1, poet: 1 |
| physician | female | 82.4 (122/148; 75.5–87.7) | 0.8 (13/1695; 0.4–1.3) | 90.4 (122/135; 84.2–94.3) | surgeon: 10, nurse: 7, professor: 4 |
| physician | male | 58.6 (89/152; 50.6–66.1) | 0.8 (16/2003; 0.5–1.3) | 84.8 (89/105; 76.7–90.4) | surgeon: 34, chiropractor: 11, professor: 11 |
| poet | female | 89.8 (44/49; 78.2–95.6) | 0.4 (7/1794; 0.2–0.8) | 86.3 (44/51; 74.3–93.2) | painter: 2, comedian: 1, yoga_teacher: 1 |
| poet | male | 78.4 (40/51; 65.4–87.5) | 0.4 (9/2104; 0.2–0.8) | 81.6 (40/49; 68.6–90.0) | journalist: 4, rapper: 4, professor: 2 |
| professor | female | 91.5 (248/271; 87.6–94.3) | 1.6 (25/1572; 1.1–2.3) | 90.8 (248/273; 86.8–93.7) | teacher: 4, journalist: 4, psychologist: 2 |
| professor | male | 89.1 (293/329; 85.2–92.0) | 2.4 (43/1826; 1.8–3.2) | 87.2 (293/336; 83.2–90.4) | surgeon: 7, attorney: 4, journalist: 3 |
| psychologist | female | 73.4 (47/64; 61.5–82.7) | 0.6 (10/1779; 0.3–1.0) | 82.5 (47/57; 70.6–90.2) | professor: 7, yoga_teacher: 2, nurse: 2 |
| psychologist | male | 79.5 (31/39; 64.5–89.2) | 0.4 (8/2116; 0.2–0.7) | 79.5 (31/39; 64.5–89.2) | professor: 2, paralegal: 1, teacher: 1 |
| rapper | female | 90.0 (9/10; 59.6–98.2) | 0.0 (0/1833; 0.0–0.2) | 100.0 (9/9; 70.1–100.0) | painter: 1 |
| rapper | male | 94.4 (85/90; 87.6–97.6) | 0.4 (8/2065; 0.2–0.8) | 91.4 (85/93; 83.9–95.6) | dj: 3, poet: 2 |
| software_engineer | female | 87.5 (14/16; 64.0–96.5) | 0.1 (1/1827; 0.0–0.3) | 93.3 (14/15; 70.2–98.8) | professor: 1, architect: 1 |
| software_engineer | male | 82.1 (69/84; 72.6–88.9) | 1.0 (20/2071; 0.6–1.5) | 77.5 (69/89; 67.8–85.0) | professor: 4, journalist: 3, architect: 2 |
| surgeon | female | 76.5 (13/17; 52.7–90.4) | 0.8 (14/1826; 0.5–1.3) | 48.1 (13/27; 30.7–66.0) | dentist: 1, physician: 1, journalist: 1 |
| surgeon | male | 84.8 (84/99; 76.5–90.6) | 2.1 (43/2056; 1.6–2.8) | 66.1 (84/127; 57.5–73.8) | physician: 6, dentist: 3, chiropractor: 1 |
| teacher | female | 61.4 (51/83; 50.7–71.2) | 0.9 (15/1760; 0.5–1.4) | 77.3 (51/66; 65.8–85.7) | pastor: 7, yoga_teacher: 6, professor: 3 |
| teacher | male | 65.5 (36/55; 52.3–76.6) | 0.6 (12/2100; 0.3–1.0) | 75.0 (36/48; 61.2–85.1) | professor: 7, unparsed: 2, pastor: 2 |
| yoga_teacher | female | 97.6 (82/84; 91.7–99.3) | 0.6 (11/1759; 0.3–1.1) | 88.2 (82/93; 80.1–93.3) | photographer: 1, nurse: 1 |
| yoga_teacher | male | 75.0 (12/16; 50.5–89.8) | 0.1 (2/2139; 0.0–0.3) | 85.7 (12/14; 60.1–96.0) | journalist: 1, professor: 1, poet: 1 |

## Llama-generated-data-filtering-GPT-full__2_original_all

| Occupation | Gender | TPR | FPR | Precision | Top three error destinations |
|---|---|---|---|---|---|
| accountant | female | 64.9 (24/37; 48.8–78.2) | 0.2 (3/1806; 0.1–0.5) | 88.9 (24/27; 71.9–96.1) | paralegal: 5, dietitian: 2, interior_designer: 2 |
| accountant | male | 68.3 (43/63; 56.0–78.4) | 0.2 (4/2092; 0.1–0.5) | 91.5 (43/47; 80.1–96.6) | attorney: 5, pastor: 4, journalist: 3 |
| architect | female | 70.8 (17/24; 50.8–85.1) | 0.3 (5/1819; 0.1–0.6) | 77.3 (17/22; 56.6–89.9) | interior_designer: 4, software_engineer: 1, journalist: 1 |
| architect | male | 61.5 (48/78; 50.4–71.6) | 0.3 (7/2077; 0.2–0.7) | 87.3 (48/55; 76.0–93.7) | software_engineer: 16, professor: 5, journalist: 2 |
| attorney | female | 87.0 (67/77; 77.7–92.8) | 0.9 (16/1766; 0.6–1.5) | 80.7 (67/83; 71.0–87.8) | paralegal: 4, professor: 2, interior_designer: 1 |
| attorney | male | 91.2 (114/125; 84.9–95.0) | 0.4 (9/2030; 0.2–0.8) | 92.7 (114/123; 86.7–96.1) | professor: 3, accountant: 2, software_engineer: 2 |
| chiropractor | female | 84.6 (22/26; 66.5–93.8) | 1.0 (18/1817; 0.6–1.6) | 55.0 (22/40; 39.8–69.3) | physician: 2, teacher: 1, personal_trainer: 1 |
| chiropractor | male | 93.2 (69/74; 85.1–97.1) | 1.2 (25/2081; 0.8–1.8) | 73.4 (69/94; 63.7–81.3) | pastor: 1, personal_trainer: 1, dietitian: 1 |
| comedian | female | 81.0 (17/21; 60.0–92.3) | 0.1 (1/1822; 0.0–0.3) | 94.4 (17/18; 74.2–99.0) | journalist: 2, paralegal: 1, filmmaker: 1 |
| comedian | male | 93.7 (74/79; 86.0–97.3) | 0.1 (2/2076; 0.0–0.4) | 97.4 (74/76; 90.9–99.3) | dj: 2, filmmaker: 1, journalist: 1 |
| composer | female | 87.5 (14/16; 64.0–96.5) | 0.0 (0/1827; 0.0–0.2) | 100.0 (14/14; 78.5–100.0) | professor: 1, teacher: 1 |
| composer | male | 96.4 (81/84; 90.0–98.8) | 0.4 (8/2071; 0.2–0.8) | 91.0 (81/89; 83.3–95.4) | rapper: 1, architect: 1, dj: 1 |
| dentist | female | 74.5 (38/51; 61.1–84.5) | 0.1 (1/1792; 0.0–0.3) | 97.4 (38/39; 86.8–99.5) | surgeon: 9, physician: 2, chiropractor: 1 |
| dentist | male | 70.5 (67/95; 60.7–78.8) | 0.1 (2/2060; 0.0–0.4) | 97.1 (67/69; 90.0–99.2) | surgeon: 19, chiropractor: 5, professor: 2 |
| dietitian | female | 92.5 (86/93; 85.3–96.3) | 0.7 (13/1750; 0.4–1.3) | 86.9 (86/99; 78.8–92.2) | personal_trainer: 1, physician: 1, psychologist: 1 |
| dietitian | male | 71.4 (5/7; 35.9–91.8) | 0.1 (2/2148; 0.0–0.3) | 71.4 (5/7; 35.9–91.8) | personal_trainer: 1, chiropractor: 1 |
| dj | female | 85.7 (12/14; 60.1–96.0) | 0.2 (3/1829; 0.1–0.5) | 80.0 (12/15; 54.8–93.0) | model: 1, software_engineer: 1 |
| dj | male | 91.9 (79/86; 84.1–96.0) | 1.1 (22/2069; 0.7–1.6) | 78.2 (79/101; 69.2–85.2) | personal_trainer: 1, architect: 1, rapper: 1 |
| filmmaker | female | 90.9 (30/33; 76.4–96.9) | 0.3 (6/1810; 0.2–0.7) | 83.3 (30/36; 68.1–92.1) | psychologist: 1, journalist: 1, teacher: 1 |
| filmmaker | male | 92.5 (62/67; 83.7–96.8) | 0.5 (11/2088; 0.3–0.9) | 84.9 (62/73; 75.0–91.4) | photographer: 2, teacher: 1, journalist: 1 |
| interior_designer | female | 87.7 (71/81; 78.7–93.2) | 1.1 (19/1762; 0.7–1.7) | 78.9 (71/90; 69.4–86.0) | architect: 3, model: 2, accountant: 1 |
| interior_designer | male | 84.2 (16/19; 62.4–94.5) | 0.1 (2/2136; 0.0–0.3) | 88.9 (16/18; 67.2–96.9) | architect: 2, attorney: 1 |
| journalist | female | 80.8 (80/99; 72.0–87.4) | 0.7 (12/1744; 0.4–1.2) | 87.0 (80/92; 78.6–92.4) | teacher: 5, software_engineer: 4, dj: 2 |
| journalist | male | 82.4 (84/102; 73.8–88.5) | 1.0 (20/2053; 0.6–1.5) | 80.8 (84/104; 72.2–87.2) | professor: 9, filmmaker: 2, dj: 2 |
| model | female | 85.5 (71/83; 76.4–91.5) | 0.2 (4/1760; 0.1–0.6) | 94.7 (71/75; 87.1–97.9) | dietitian: 2, interior_designer: 2, personal_trainer: 1 |
| model | male | 82.4 (14/17; 59.0–93.8) | 0.3 (7/2138; 0.2–0.7) | 66.7 (14/21; 45.4–82.8) | professor: 1, journalist: 1, comedian: 1 |
| nurse | female | 79.3 (138/174; 72.7–84.7) | 0.5 (8/1669; 0.2–0.9) | 94.5 (138/146; 89.6–97.2) | chiropractor: 8, physician: 8, paralegal: 3 |
| nurse | male | 76.5 (13/17; 52.7–90.4) | 0.0 (1/2138; 0.0–0.3) | 92.9 (13/14; 68.5–98.7) | chiropractor: 2, psychologist: 1, software_engineer: 1 |
| painter | female | 89.1 (41/46; 77.0–95.3) | 0.4 (7/1797; 0.2–0.8) | 85.4 (41/48; 72.8–92.8) | professor: 2, interior_designer: 1, filmmaker: 1 |
| painter | male | 85.2 (46/54; 73.4–92.3) | 0.2 (5/2101; 0.1–0.6) | 90.2 (46/51; 79.0–95.7) | photographer: 5, unparsed: 1, software_engineer: 1 |
| paralegal | female | 84.7 (72/85; 75.6–90.8) | 1.1 (19/1758; 0.7–1.7) | 79.1 (72/91; 69.7–86.2) | attorney: 10, journalist: 1, interior_designer: 1 |
| paralegal | male | 73.3 (11/15; 48.0–89.1) | 0.1 (2/2140; 0.0–0.3) | 84.6 (11/13; 57.8–95.7) | attorney: 3, software_engineer: 1 |
| pastor | female | 91.7 (22/24; 74.2–97.7) | 0.5 (10/1819; 0.3–1.0) | 68.8 (22/32; 51.4–82.0) | teacher: 1, interior_designer: 1 |
| pastor | male | 88.2 (67/76; 79.0–93.6) | 0.7 (14/2079; 0.4–1.1) | 82.7 (67/81; 73.1–89.4) | teacher: 2, journalist: 1, composer: 1 |
| personal_trainer | female | 95.7 (44/46; 85.5–98.8) | 0.3 (5/1797; 0.1–0.6) | 89.8 (44/49; 78.2–95.6) | journalist: 1, pastor: 1 |
| personal_trainer | male | 92.5 (49/53; 82.1–97.0) | 0.2 (5/2102; 0.1–0.6) | 90.7 (49/54; 80.1–96.0) | chiropractor: 2, model: 2 |
| photographer | female | 93.0 (66/71; 84.6–97.0) | 0.4 (7/1772; 0.2–0.8) | 90.4 (66/73; 81.5–95.3) | dietitian: 2, painter: 2, architect: 1 |
| photographer | male | 93.0 (120/129; 87.3–96.3) | 0.8 (16/2026; 0.5–1.3) | 88.2 (120/136; 81.7–92.6) | filmmaker: 3, painter: 2, journalist: 2 |
| physician | female | 90.5 (134/148; 84.7–94.3) | 1.0 (17/1695; 0.6–1.6) | 88.7 (134/151; 82.7–92.9) | chiropractor: 5, nurse: 4, surgeon: 2 |
| physician | male | 79.6 (121/152; 72.5–85.2) | 0.9 (18/2003; 0.6–1.4) | 87.1 (121/139; 80.5–91.6) | chiropractor: 11, surgeon: 10, professor: 7 |
| poet | female | 65.3 (32/49; 51.3–77.1) | 0.1 (1/1794; 0.0–0.3) | 97.0 (32/33; 84.7–99.5) | teacher: 7, professor: 4, journalist: 2 |
| poet | male | 64.7 (33/51; 51.0–76.4) | 0.0 (1/2104; 0.0–0.3) | 97.1 (33/34; 85.1–99.5) | rapper: 5, journalist: 4, professor: 3 |
| professor | female | 92.6 (251/271; 88.9–95.2) | 1.8 (29/1572; 1.3–2.6) | 89.6 (251/280; 85.5–92.7) | teacher: 6, psychologist: 3, physician: 2 |
| professor | male | 90.3 (297/329; 86.6–93.0) | 2.7 (50/1826; 2.1–3.6) | 85.6 (297/347; 81.5–88.9) | physician: 7, surgeon: 6, journalist: 2 |
| psychologist | female | 79.7 (51/64; 68.3–87.7) | 0.4 (7/1779; 0.2–0.8) | 87.9 (51/58; 77.1–94.0) | professor: 5, teacher: 2, paralegal: 1 |
| psychologist | male | 74.4 (29/39; 58.9–85.4) | 0.4 (9/2116; 0.2–0.8) | 76.3 (29/38; 60.8–87.0) | professor: 4, teacher: 2, personal_trainer: 1 |
| rapper | female | 90.0 (9/10; 59.6–98.2) | 0.1 (1/1833; 0.0–0.3) | 90.0 (9/10; 59.6–98.2) | painter: 1 |
| rapper | male | 84.4 (76/90; 75.6–90.5) | 0.4 (8/2065; 0.2–0.8) | 90.5 (76/84; 82.3–95.1) | dj: 12, poet: 1, filmmaker: 1 |
| software_engineer | female | 87.5 (14/16; 64.0–96.5) | 0.5 (9/1827; 0.3–0.9) | 60.9 (14/23; 40.8–77.8) | paralegal: 1, professor: 1 |
| software_engineer | male | 90.5 (76/84; 82.3–95.1) | 1.3 (26/2071; 0.9–1.8) | 74.5 (76/102; 65.3–82.0) | professor: 2, teacher: 2, psychologist: 1 |
| surgeon | female | 76.5 (13/17; 52.7–90.4) | 0.7 (12/1826; 0.4–1.1) | 52.0 (13/25; 33.5–70.0) | chiropractor: 3, physician: 1 |
| surgeon | male | 80.8 (80/99; 72.0–87.4) | 1.8 (36/2056; 1.3–2.4) | 69.0 (80/116; 60.1–76.7) | physician: 9, professor: 3, chiropractor: 2 |
| teacher | female | 60.2 (50/83; 49.5–70.1) | 1.7 (30/1760; 1.2–2.4) | 62.5 (50/80; 51.5–72.3) | yoga_teacher: 6, pastor: 5, professor: 5 |
| teacher | male | 67.3 (37/55; 54.1–78.2) | 0.5 (11/2100; 0.3–0.9) | 77.1 (37/48; 63.5–86.7) | professor: 8, composer: 2, pastor: 2 |
| yoga_teacher | female | 97.6 (82/84; 91.7–99.3) | 0.5 (9/1759; 0.3–1.0) | 90.1 (82/91; 82.3–94.7) | personal_trainer: 1, dietitian: 1 |
| yoga_teacher | male | 87.5 (14/16; 64.0–96.5) | 0.2 (4/2139; 0.1–0.5) | 77.8 (14/18; 54.8–91.0) | software_engineer: 1, dietitian: 1 |

## Llama-generated-data-filtering-GPT-full__3_original_content_only

| Occupation | Gender | TPR | FPR | Precision | Top three error destinations |
|---|---|---|---|---|---|
| accountant | female | 75.7 (28/37; 59.9–86.6) | 0.7 (12/1806; 0.4–1.2) | 70.0 (28/40; 54.6–81.9) | journalist: 2, physician: 2, paralegal: 2 |
| accountant | male | 74.6 (47/63; 62.7–83.7) | 0.3 (7/2092; 0.2–0.7) | 87.0 (47/54; 75.6–93.6) | journalist: 4, attorney: 4, architect: 3 |
| architect | female | 66.7 (16/24; 46.7–82.0) | 0.4 (7/1819; 0.2–0.8) | 69.6 (16/23; 49.1–84.4) | interior_designer: 5, software_engineer: 1, accountant: 1 |
| architect | male | 69.2 (54/78; 58.3–78.4) | 0.8 (16/2077; 0.5–1.2) | 77.1 (54/70; 66.0–85.4) | software_engineer: 11, professor: 5, interior_designer: 3 |
| attorney | female | 85.7 (66/77; 76.2–91.8) | 0.7 (13/1766; 0.4–1.3) | 83.5 (66/79; 73.9–90.1) | professor: 3, paralegal: 3, accountant: 2 |
| attorney | male | 88.8 (111/125; 82.1–93.2) | 0.5 (11/2030; 0.3–1.0) | 91.0 (111/122; 84.6–94.9) | professor: 3, journalist: 2, accountant: 2 |
| chiropractor | female | 73.1 (19/26; 53.9–86.3) | 0.2 (4/1817; 0.1–0.6) | 82.6 (19/23; 62.9–93.0) | nurse: 4, physician: 3 |
| chiropractor | male | 83.8 (62/74; 73.8–90.5) | 0.8 (16/2081; 0.5–1.2) | 79.5 (62/78; 69.2–87.0) | physician: 6, pastor: 1, personal_trainer: 1 |
| comedian | female | 81.0 (17/21; 60.0–92.3) | 0.2 (3/1822; 0.1–0.5) | 85.0 (17/20; 64.0–94.8) | journalist: 2, nurse: 1, model: 1 |
| comedian | male | 94.9 (75/79; 87.7–98.0) | 0.4 (8/2076; 0.2–0.8) | 90.4 (75/83; 82.1–95.0) | dj: 1, journalist: 1, model: 1 |
| composer | female | 81.2 (13/16; 57.0–93.4) | 0.2 (3/1827; 0.1–0.5) | 81.2 (13/16; 57.0–93.4) | comedian: 1, poet: 1, teacher: 1 |
| composer | male | 92.9 (78/84; 85.3–96.7) | 0.4 (9/2071; 0.2–0.8) | 89.7 (78/87; 81.5–94.5) | rapper: 1, painter: 1, teacher: 1 |
| dentist | female | 86.3 (44/51; 74.3–93.2) | 0.1 (2/1792; 0.0–0.4) | 95.7 (44/46; 85.5–98.8) | physician: 3, professor: 1, nurse: 1 |
| dentist | male | 91.6 (87/95; 84.3–95.7) | 0.2 (4/2060; 0.1–0.5) | 95.6 (87/91; 89.2–98.3) | chiropractor: 3, physician: 2, psychologist: 1 |
| dietitian | female | 89.2 (83/93; 81.3–94.1) | 0.3 (5/1750; 0.1–0.7) | 94.3 (83/88; 87.4–97.5) | nurse: 3, physician: 2, psychologist: 2 |
| dietitian | male | 85.7 (6/7; 48.7–97.4) | 0.0 (0/2148; 0.0–0.2) | 100.0 (6/6; 61.0–100.0) | physician: 1 |
| dj | female | 78.6 (11/14; 52.4–92.4) | 0.0 (0/1829; 0.0–0.2) | 100.0 (11/11; 74.1–100.0) | model: 1, accountant: 1, composer: 1 |
| dj | male | 87.2 (75/86; 78.5–92.7) | 0.3 (6/2069; 0.1–0.6) | 92.6 (75/81; 84.8–96.6) | rapper: 3, personal_trainer: 1, poet: 1 |
| filmmaker | female | 78.8 (26/33; 62.2–89.3) | 0.1 (1/1810; 0.0–0.3) | 96.3 (26/27; 81.7–99.3) | teacher: 2, psychologist: 2, photographer: 1 |
| filmmaker | male | 88.1 (59/67; 78.2–93.8) | 0.1 (3/2088; 0.0–0.4) | 95.2 (59/62; 86.7–98.3) | photographer: 3, professor: 2, painter: 1 |
| interior_designer | female | 86.4 (70/81; 77.3–92.2) | 0.8 (14/1762; 0.5–1.3) | 83.3 (70/84; 73.9–89.8) | model: 4, architect: 3, journalist: 2 |
| interior_designer | male | 78.9 (15/19; 56.7–91.5) | 0.1 (3/2136; 0.0–0.4) | 83.3 (15/18; 60.8–94.2) | architect: 3, attorney: 1 |
| journalist | female | 82.8 (82/99; 74.2–89.0) | 1.0 (18/1744; 0.7–1.6) | 82.0 (82/100; 73.3–88.3) | nurse: 2, interior_designer: 2, photographer: 2 |
| journalist | male | 89.2 (91/102; 81.7–93.9) | 1.1 (22/2053; 0.7–1.6) | 80.5 (91/113; 72.3–86.8) | professor: 4, photographer: 3, teacher: 1 |
| model | female | 88.0 (73/83; 79.2–93.3) | 0.6 (11/1760; 0.3–1.1) | 86.9 (73/84; 78.1–92.5) | journalist: 2, personal_trainer: 1, comedian: 1 |
| model | male | 76.5 (13/17; 52.7–90.4) | 0.2 (5/2138; 0.1–0.5) | 72.2 (13/18; 49.1–87.5) | professor: 2, pastor: 1, attorney: 1 |
| nurse | female | 91.4 (159/174; 86.3–94.7) | 2.8 (46/1669; 2.1–3.7) | 77.6 (159/205; 71.4–82.7) | professor: 5, teacher: 2, chiropractor: 1 |
| nurse | male | 70.6 (12/17; 46.9–86.7) | 0.2 (4/2138; 0.1–0.5) | 75.0 (12/16; 50.5–89.8) | chiropractor: 3, psychologist: 1, physician: 1 |
| painter | female | 91.3 (42/46; 79.7–96.6) | 0.4 (7/1797; 0.2–0.8) | 85.7 (42/49; 73.3–92.9) | photographer: 2, poet: 1, interior_designer: 1 |
| painter | male | 87.0 (47/54; 75.6–93.6) | 0.2 (5/2101; 0.1–0.6) | 90.4 (47/52; 79.4–95.8) | photographer: 4, unparsed: 1, architect: 1 |
| paralegal | female | 84.7 (72/85; 75.6–90.8) | 0.4 (7/1758; 0.2–0.8) | 91.1 (72/79; 82.8–95.6) | attorney: 9, nurse: 1, psychologist: 1 |
| paralegal | male | 66.7 (10/15; 41.7–84.8) | 0.1 (2/2140; 0.0–0.3) | 83.3 (10/12; 55.2–95.3) | attorney: 4, pastor: 1 |
| pastor | female | 83.3 (20/24; 64.1–93.3) | 0.3 (6/1819; 0.2–0.7) | 76.9 (20/26; 57.9–89.0) | nurse: 2, teacher: 1, interior_designer: 1 |
| pastor | male | 85.5 (65/76; 75.9–91.7) | 0.6 (13/2079; 0.4–1.1) | 83.3 (65/78; 73.5–90.0) | comedian: 3, journalist: 2, professor: 2 |
| personal_trainer | female | 84.8 (39/46; 71.8–92.4) | 0.3 (5/1797; 0.1–0.6) | 88.6 (39/44; 76.0–95.0) | nurse: 3, pastor: 1, model: 1 |
| personal_trainer | male | 90.6 (48/53; 79.7–95.9) | 0.2 (4/2102; 0.1–0.5) | 92.3 (48/52; 81.8–97.0) | chiropractor: 3, model: 2 |
| photographer | female | 90.1 (64/71; 81.0–95.1) | 0.6 (11/1772; 0.3–1.1) | 85.3 (64/75; 75.6–91.6) | painter: 3, nurse: 2, architect: 1 |
| photographer | male | 93.8 (121/129; 88.2–96.8) | 0.7 (15/2026; 0.4–1.2) | 89.0 (121/136; 82.6–93.2) | journalist: 3, poet: 1, model: 1 |
| physician | female | 87.2 (129/148; 80.8–91.6) | 1.0 (17/1695; 0.6–1.6) | 88.4 (129/146; 82.1–92.6) | nurse: 14, professor: 3, dentist: 1 |
| physician | male | 81.6 (124/152; 74.7–86.9) | 1.6 (33/2003; 1.2–2.3) | 79.0 (124/157; 72.0–84.6) | professor: 9, surgeon: 7, chiropractor: 6 |
| poet | female | 91.8 (45/49; 80.8–96.8) | 0.8 (14/1794; 0.5–1.3) | 76.3 (45/59; 64.0–85.3) | painter: 2, dietitian: 1, photographer: 1 |
| poet | male | 80.4 (41/51; 67.5–89.0) | 0.5 (11/2104; 0.3–0.9) | 78.8 (41/52; 66.0–87.8) | rapper: 3, journalist: 2, unparsed: 2 |
| professor | female | 91.1 (247/271; 87.2–94.0) | 2.0 (32/1572; 1.4–2.9) | 88.5 (247/279; 84.3–91.8) | teacher: 5, poet: 4, psychologist: 3 |
| professor | male | 90.0 (296/329; 86.2–92.8) | 3.0 (54/1826; 2.3–3.8) | 84.6 (296/350; 80.4–88.0) | physician: 5, surgeon: 5, journalist: 3 |
| psychologist | female | 75.0 (48/64; 63.2–84.0) | 0.6 (11/1779; 0.3–1.1) | 81.4 (48/59; 69.6–89.3) | professor: 8, nurse: 2, accountant: 1 |
| psychologist | male | 74.4 (29/39; 58.9–85.4) | 0.5 (10/2116; 0.3–0.9) | 74.4 (29/39; 58.9–85.4) | professor: 4, accountant: 1, teacher: 1 |
| rapper | female | 90.0 (9/10; 59.6–98.2) | 0.0 (0/1833; 0.0–0.2) | 100.0 (9/9; 70.1–100.0) | painter: 1 |
| rapper | male | 92.2 (83/90; 84.8–96.2) | 0.3 (7/2065; 0.2–0.7) | 92.2 (83/90; 84.8–96.2) | dj: 3, poet: 2, comedian: 1 |
| software_engineer | female | 81.2 (13/16; 57.0–93.4) | 0.1 (2/1827; 0.0–0.4) | 86.7 (13/15; 62.1–96.3) | paralegal: 1, professor: 1, architect: 1 |
| software_engineer | male | 84.5 (71/84; 75.3–90.7) | 0.8 (16/2071; 0.5–1.3) | 81.6 (71/87; 72.2–88.4) | architect: 5, professor: 3, accountant: 1 |
| surgeon | female | 41.2 (7/17; 21.6–64.0) | 0.2 (3/1826; 0.1–0.5) | 70.0 (7/10; 39.7–89.2) | physician: 4, nurse: 2, professor: 2 |
| surgeon | male | 74.7 (74/99; 65.4–82.3) | 0.7 (14/2056; 0.4–1.1) | 84.1 (74/88; 75.0–90.3) | physician: 14, professor: 5, dentist: 3 |
| teacher | female | 59.0 (49/83; 48.3–69.0) | 0.9 (15/1760; 0.5–1.4) | 76.6 (49/64; 64.9–85.3) | journalist: 6, poet: 5, yoga_teacher: 4 |
| teacher | male | 63.6 (35/55; 50.4–75.1) | 0.3 (7/2100; 0.2–0.7) | 83.3 (35/42; 69.4–91.7) | professor: 7, composer: 2, unparsed: 2 |
| yoga_teacher | female | 91.7 (77/84; 83.8–95.9) | 0.2 (4/1759; 0.1–0.6) | 95.1 (77/81; 88.0–98.1) | personal_trainer: 3, photographer: 1, professor: 1 |
| yoga_teacher | male | 75.0 (12/16; 50.5–89.8) | 0.1 (2/2139; 0.0–0.3) | 85.7 (12/14; 60.1–96.0) | software_engineer: 1, professor: 1, poet: 1 |

## Llama-generated-data-filtering-GPT-full__4_original_content_explanation

| Occupation | Gender | TPR | FPR | Precision | Top three error destinations |
|---|---|---|---|---|---|
| accountant | female | 73.0 (27/37; 57.0–84.6) | 0.6 (11/1806; 0.3–1.1) | 71.1 (27/38; 55.2–83.0) | journalist: 2, model: 2, physician: 2 |
| accountant | male | 66.7 (42/63; 54.4–77.1) | 0.3 (7/2092; 0.2–0.7) | 85.7 (42/49; 73.3–92.9) | attorney: 6, journalist: 4, pastor: 3 |
| architect | female | 66.7 (16/24; 46.7–82.0) | 0.2 (4/1819; 0.1–0.6) | 80.0 (16/20; 58.4–91.9) | interior_designer: 5, software_engineer: 2, accountant: 1 |
| architect | male | 62.8 (49/78; 51.7–72.7) | 0.4 (9/2077; 0.2–0.8) | 84.5 (49/58; 73.1–91.6) | software_engineer: 14, professor: 5, interior_designer: 4 |
| attorney | female | 84.4 (65/77; 74.7–90.9) | 0.8 (15/1766; 0.5–1.4) | 81.2 (65/80; 71.3–88.3) | paralegal: 3, teacher: 2, accountant: 2 |
| attorney | male | 88.8 (111/125; 82.1–93.2) | 0.7 (15/2030; 0.4–1.2) | 88.1 (111/126; 81.3–92.7) | accountant: 4, professor: 3, unparsed: 2 |
| chiropractor | female | 80.8 (21/26; 62.1–91.5) | 0.6 (11/1817; 0.3–1.1) | 65.6 (21/32; 48.3–79.6) | physician: 4, unparsed: 1 |
| chiropractor | male | 83.8 (62/74; 73.8–90.5) | 1.0 (20/2081; 0.6–1.5) | 75.6 (62/82; 65.3–83.6) | physician: 6, pastor: 1, personal_trainer: 1 |
| comedian | female | 81.0 (17/21; 60.0–92.3) | 0.1 (2/1822; 0.0–0.4) | 89.5 (17/19; 68.6–97.1) | nurse: 1, pastor: 1, professor: 1 |
| comedian | male | 93.7 (74/79; 86.0–97.3) | 0.2 (4/2076; 0.1–0.5) | 94.9 (74/78; 87.5–98.0) | dj: 2, composer: 1, psychologist: 1 |
| composer | female | 87.5 (14/16; 64.0–96.5) | 0.0 (0/1827; 0.0–0.2) | 100.0 (14/14; 78.5–100.0) | professor: 1, teacher: 1 |
| composer | male | 97.6 (82/84; 91.7–99.3) | 0.5 (10/2071; 0.3–0.9) | 89.1 (82/92; 81.1–94.0) | model: 1, painter: 1 |
| dentist | female | 88.2 (45/51; 76.6–94.5) | 0.1 (1/1792; 0.0–0.3) | 97.8 (45/46; 88.7–99.6) | physician: 2, professor: 1, nurse: 1 |
| dentist | male | 90.5 (86/95; 83.0–94.9) | 0.2 (4/2060; 0.1–0.5) | 95.6 (86/90; 89.1–98.3) | chiropractor: 4, physician: 2, photographer: 1 |
| dietitian | female | 94.6 (88/93; 88.0–97.7) | 0.4 (7/1750; 0.2–0.8) | 92.6 (88/95; 85.6–96.4) | nurse: 2, physician: 1, professor: 1 |
| dietitian | male | 85.7 (6/7; 48.7–97.4) | 0.0 (1/2148; 0.0–0.3) | 85.7 (6/7; 48.7–97.4) | physician: 1 |
| dj | female | 78.6 (11/14; 52.4–92.4) | 0.0 (0/1829; 0.0–0.2) | 100.0 (11/11; 74.1–100.0) | model: 2, teacher: 1 |
| dj | male | 90.7 (78/86; 82.7–95.2) | 0.4 (8/2069; 0.2–0.8) | 90.7 (78/86; 82.7–95.2) | personal_trainer: 1, teacher: 1, architect: 1 |
| filmmaker | female | 84.8 (28/33; 69.1–93.3) | 0.2 (3/1810; 0.1–0.5) | 90.3 (28/31; 75.1–96.7) | psychologist: 2, professor: 1, journalist: 1 |
| filmmaker | male | 88.1 (59/67; 78.2–93.8) | 0.2 (4/2088; 0.1–0.5) | 93.7 (59/63; 84.8–97.5) | journalist: 3, photographer: 2, professor: 2 |
| interior_designer | female | 85.2 (69/81; 75.9–91.3) | 0.9 (16/1762; 0.6–1.5) | 81.2 (69/85; 71.6–88.1) | model: 3, nurse: 2, journalist: 2 |
| interior_designer | male | 89.5 (17/19; 68.6–97.1) | 0.2 (5/2136; 0.1–0.5) | 77.3 (17/22; 56.6–89.9) | attorney: 1, architect: 1 |
| journalist | female | 81.8 (81/99; 73.1–88.2) | 0.8 (14/1744; 0.5–1.3) | 85.3 (81/95; 76.8–91.0) | interior_designer: 3, professor: 3, filmmaker: 2 |
| journalist | male | 88.2 (90/102; 80.6–93.1) | 1.3 (27/2053; 0.9–1.9) | 76.9 (90/117; 68.5–83.6) | professor: 5, photographer: 2, teacher: 1 |
| model | female | 90.4 (75/83; 82.1–95.0) | 0.9 (15/1760; 0.5–1.4) | 83.3 (75/90; 74.3–89.6) | yoga_teacher: 1, comedian: 1, nurse: 1 |
| model | male | 76.5 (13/17; 52.7–90.4) | 0.3 (7/2138; 0.2–0.7) | 65.0 (13/20; 43.3–81.9) | professor: 2, journalist: 1, attorney: 1 |
| nurse | female | 82.8 (144/174; 76.5–87.6) | 1.6 (27/1669; 1.1–2.3) | 84.2 (144/171; 78.0–88.9) | physician: 8, professor: 6, chiropractor: 4 |
| nurse | male | 76.5 (13/17; 52.7–90.4) | 0.2 (5/2138; 0.1–0.5) | 72.2 (13/18; 49.1–87.5) | chiropractor: 3, physician: 1 |
| painter | female | 89.1 (41/46; 77.0–95.3) | 0.3 (6/1797; 0.2–0.7) | 87.2 (41/47; 74.8–94.0) | photographer: 3, poet: 1, interior_designer: 1 |
| painter | male | 85.2 (46/54; 73.4–92.3) | 0.2 (5/2101; 0.1–0.6) | 90.2 (46/51; 79.0–95.7) | photographer: 5, unparsed: 1, poet: 1 |
| paralegal | female | 83.5 (71/85; 74.2–89.9) | 0.2 (4/1758; 0.1–0.6) | 94.7 (71/75; 87.1–97.9) | attorney: 9, accountant: 1, journalist: 1 |
| paralegal | male | 66.7 (10/15; 41.7–84.8) | 0.0 (0/2140; 0.0–0.2) | 100.0 (10/10; 72.2–100.0) | attorney: 3, software_engineer: 1, unparsed: 1 |
| pastor | female | 95.8 (23/24; 79.8–99.3) | 0.5 (9/1819; 0.3–0.9) | 71.9 (23/32; 54.6–84.4) | interior_designer: 1 |
| pastor | male | 90.8 (69/76; 82.2–95.5) | 0.6 (13/2079; 0.4–1.1) | 84.1 (69/82; 74.7–90.5) | journalist: 2, teacher: 1, accountant: 1 |
| personal_trainer | female | 87.0 (40/46; 74.3–93.9) | 0.1 (1/1797; 0.0–0.3) | 97.6 (40/41; 87.4–99.6) | dietitian: 2, nurse: 1, pastor: 1 |
| personal_trainer | male | 88.7 (47/53; 77.4–94.7) | 0.2 (4/2102; 0.1–0.5) | 92.2 (47/51; 81.5–96.9) | chiropractor: 3, model: 2, surgeon: 1 |
| photographer | female | 88.7 (63/71; 79.3–94.2) | 0.5 (9/1772; 0.3–1.0) | 87.5 (63/72; 77.9–93.3) | nurse: 3, painter: 2, architect: 1 |
| photographer | male | 91.5 (118/129; 85.4–95.2) | 0.7 (15/2026; 0.4–1.2) | 88.7 (118/133; 82.2–93.0) | journalist: 5, model: 2, attorney: 1 |
| physician | female | 88.5 (131/148; 82.4–92.7) | 1.4 (23/1695; 0.9–2.0) | 85.1 (131/154; 78.6–89.8) | nurse: 5, chiropractor: 5, professor: 4 |
| physician | male | 77.0 (117/152; 69.7–83.0) | 1.3 (26/2003; 0.9–1.9) | 81.8 (117/143; 74.7–87.3) | surgeon: 10, professor: 10, chiropractor: 7 |
| poet | female | 87.8 (43/49; 75.8–94.3) | 0.4 (7/1794; 0.2–0.8) | 86.0 (43/50; 73.8–93.0) | professor: 2, painter: 1, journalist: 1 |
| poet | male | 66.7 (34/51; 53.0–78.0) | 0.3 (7/2104; 0.2–0.7) | 82.9 (34/41; 68.7–91.5) | professor: 6, rapper: 4, journalist: 3 |
| professor | female | 96.7 (262/271; 93.8–98.2) | 2.4 (38/1572; 1.8–3.3) | 87.3 (262/300; 83.1–90.6) | teacher: 3, nurse: 2, psychologist: 1 |
| professor | male | 92.7 (305/329; 89.4–95.0) | 3.2 (59/1826; 2.5–4.1) | 83.8 (305/364; 79.7–87.2) | journalist: 3, surgeon: 3, attorney: 3 |
| psychologist | female | 70.3 (45/64; 58.2–80.1) | 0.4 (8/1779; 0.2–0.9) | 84.9 (45/53; 72.9–92.1) | professor: 8, physician: 3, teacher: 2 |
| psychologist | male | 74.4 (29/39; 58.9–85.4) | 0.3 (6/2116; 0.1–0.6) | 82.9 (29/35; 67.3–91.9) | professor: 5, personal_trainer: 1, teacher: 1 |
| rapper | female | 80.0 (8/10; 49.0–94.3) | 0.1 (1/1833; 0.0–0.3) | 88.9 (8/9; 56.5–98.0) | unparsed: 1, painter: 1 |
| rapper | male | 90.0 (81/90; 82.1–94.6) | 0.2 (5/2065; 0.1–0.6) | 94.2 (81/86; 87.1–97.5) | dj: 6, poet: 2, comedian: 1 |
| software_engineer | female | 81.2 (13/16; 57.0–93.4) | 0.2 (3/1827; 0.1–0.5) | 81.2 (13/16; 57.0–93.4) | accountant: 1, professor: 1, architect: 1 |
| software_engineer | male | 82.1 (69/84; 72.6–88.9) | 0.9 (19/2071; 0.6–1.4) | 78.4 (69/88; 68.7–85.7) | professor: 4, architect: 3, composer: 2 |
| surgeon | female | 52.9 (9/17; 31.0–73.8) | 0.2 (3/1826; 0.1–0.5) | 75.0 (9/12; 46.8–91.1) | physician: 3, professor: 2, dentist: 1 |
| surgeon | male | 78.8 (78/99; 69.7–85.7) | 0.9 (18/2056; 0.6–1.4) | 81.2 (78/96; 72.3–87.8) | physician: 11, dentist: 4, professor: 3 |
| teacher | female | 56.6 (47/83; 45.9–66.8) | 0.8 (14/1760; 0.5–1.3) | 77.0 (47/61; 65.1–85.8) | professor: 6, pastor: 5, yoga_teacher: 5 |
| teacher | male | 56.4 (31/55; 43.3–68.6) | 0.4 (9/2100; 0.2–0.8) | 77.5 (31/40; 62.5–87.7) | professor: 9, pastor: 3, composer: 2 |
| yoga_teacher | female | 95.2 (80/84; 88.4–98.1) | 0.5 (8/1759; 0.2–0.9) | 90.9 (80/88; 83.1–95.3) | photographer: 1, personal_trainer: 1, comedian: 1 |
| yoga_teacher | male | 87.5 (14/16; 64.0–96.5) | 0.2 (4/2139; 0.1–0.5) | 77.8 (14/18; 54.8–91.0) | poet: 1, professor: 1 |

## Llama-generated-data-filtering-GPT-full__5_original_random

| Occupation | Gender | TPR | FPR | Precision | Top three error destinations |
|---|---|---|---|---|---|
| accountant | female | 67.6 (25/37; 51.5–80.4) | 0.6 (10/1806; 0.3–1.0) | 71.4 (25/35; 54.9–83.7) | photographer: 2, physician: 2, interior_designer: 2 |
| accountant | male | 63.5 (40/63; 51.1–74.3) | 0.4 (9/2092; 0.2–0.8) | 81.6 (40/49; 68.6–90.0) | attorney: 7, pastor: 5, professor: 3 |
| architect | female | 70.8 (17/24; 50.8–85.1) | 0.3 (5/1819; 0.1–0.6) | 77.3 (17/22; 56.6–89.9) | interior_designer: 4, software_engineer: 1, professor: 1 |
| architect | male | 69.2 (54/78; 58.3–78.4) | 1.1 (23/2077; 0.7–1.7) | 70.1 (54/77; 59.2–79.2) | software_engineer: 8, professor: 5, interior_designer: 3 |
| attorney | female | 85.7 (66/77; 76.2–91.8) | 0.6 (10/1766; 0.3–1.0) | 86.8 (66/76; 77.4–92.7) | paralegal: 4, accountant: 2, professor: 1 |
| attorney | male | 85.6 (107/125; 78.4–90.7) | 0.7 (15/2030; 0.4–1.2) | 87.7 (107/122; 80.7–92.4) | accountant: 5, professor: 4, journalist: 2 |
| chiropractor | female | 80.8 (21/26; 62.1–91.5) | 0.3 (6/1817; 0.2–0.7) | 77.8 (21/27; 59.2–89.4) | physician: 2, unparsed: 1, nurse: 1 |
| chiropractor | male | 89.2 (66/74; 80.1–94.4) | 1.1 (23/2081; 0.7–1.7) | 74.2 (66/89; 64.2–82.1) | physician: 3, professor: 2, pastor: 1 |
| comedian | female | 81.0 (17/21; 60.0–92.3) | 0.1 (2/1822; 0.0–0.4) | 89.5 (17/19; 68.6–97.1) | nurse: 2, journalist: 1, filmmaker: 1 |
| comedian | male | 94.9 (75/79; 87.7–98.0) | 0.1 (3/2076; 0.0–0.4) | 96.2 (75/78; 89.3–98.7) | dj: 1, psychologist: 1, filmmaker: 1 |
| composer | female | 93.8 (15/16; 71.7–98.9) | 0.0 (0/1827; 0.0–0.2) | 100.0 (15/15; 79.6–100.0) | teacher: 1 |
| composer | male | 92.9 (78/84; 85.3–96.7) | 0.4 (8/2071; 0.2–0.8) | 90.7 (78/86; 82.7–95.2) | dj: 2, poet: 1, architect: 1 |
| dentist | female | 94.1 (48/51; 84.1–98.0) | 0.1 (2/1792; 0.0–0.4) | 96.0 (48/50; 86.5–98.9) | professor: 1, pastor: 1, surgeon: 1 |
| dentist | male | 90.5 (86/95; 83.0–94.9) | 0.2 (4/2060; 0.1–0.5) | 95.6 (86/90; 89.1–98.3) | chiropractor: 5, photographer: 1, physician: 1 |
| dietitian | female | 89.2 (83/93; 81.3–94.1) | 0.3 (5/1750; 0.1–0.7) | 94.3 (83/88; 87.4–97.5) | professor: 3, psychologist: 2, nurse: 2 |
| dietitian | male | 85.7 (6/7; 48.7–97.4) | 0.0 (0/2148; 0.0–0.2) | 100.0 (6/6; 61.0–100.0) | physician: 1 |
| dj | female | 78.6 (11/14; 52.4–92.4) | 0.0 (0/1829; 0.0–0.2) | 100.0 (11/11; 74.1–100.0) | rapper: 1, model: 1, accountant: 1 |
| dj | male | 90.7 (78/86; 82.7–95.2) | 0.3 (7/2069; 0.2–0.7) | 91.8 (78/85; 84.0–96.0) | photographer: 2, poet: 1, architect: 1 |
| filmmaker | female | 81.8 (27/33; 65.6–91.4) | 0.2 (3/1810; 0.1–0.5) | 90.0 (27/30; 74.4–96.5) | professor: 2, psychologist: 2, journalist: 1 |
| filmmaker | male | 88.1 (59/67; 78.2–93.8) | 0.3 (6/2088; 0.1–0.6) | 90.8 (59/65; 81.3–95.7) | professor: 3, photographer: 2, journalist: 2 |
| interior_designer | female | 90.1 (73/81; 81.7–94.9) | 0.8 (14/1762; 0.5–1.3) | 83.9 (73/87; 74.8–90.2) | model: 3, accountant: 1, architect: 1 |
| interior_designer | male | 84.2 (16/19; 62.4–94.5) | 0.1 (3/2136; 0.0–0.4) | 84.2 (16/19; 62.4–94.5) | architect: 2, attorney: 1 |
| journalist | female | 81.8 (81/99; 73.1–88.2) | 0.7 (13/1744; 0.4–1.3) | 86.2 (81/94; 77.8–91.7) | interior_designer: 3, model: 3, photographer: 2 |
| journalist | male | 84.3 (86/102; 76.0–90.1) | 1.0 (20/2053; 0.6–1.5) | 81.1 (86/106; 72.6–87.4) | professor: 7, poet: 2, pastor: 2 |
| model | female | 89.2 (74/83; 80.7–94.2) | 0.6 (10/1760; 0.3–1.0) | 88.1 (74/84; 79.5–93.4) | interior_designer: 2, yoga_teacher: 1, comedian: 1 |
| model | male | 76.5 (13/17; 52.7–90.4) | 0.3 (7/2138; 0.2–0.7) | 65.0 (13/20; 43.3–81.9) | professor: 2, journalist: 1, attorney: 1 |
| nurse | female | 83.9 (146/174; 77.7–88.6) | 1.1 (19/1669; 0.7–1.8) | 88.5 (146/165; 82.7–92.5) | physician: 11, professor: 8, chiropractor: 2 |
| nurse | male | 76.5 (13/17; 52.7–90.4) | 0.0 (1/2138; 0.0–0.3) | 92.9 (13/14; 68.5–98.7) | chiropractor: 3, psychologist: 1 |
| painter | female | 91.3 (42/46; 79.7–96.6) | 0.4 (7/1797; 0.2–0.8) | 85.7 (42/49; 73.3–92.9) | photographer: 2, poet: 1, interior_designer: 1 |
| painter | male | 81.5 (44/54; 69.2–89.6) | 0.2 (5/2101; 0.1–0.6) | 89.8 (44/49; 78.2–95.6) | photographer: 5, poet: 3, unparsed: 1 |
| paralegal | female | 85.9 (73/85; 76.9–91.7) | 0.4 (7/1758; 0.2–0.8) | 91.2 (73/80; 83.0–95.7) | attorney: 6, journalist: 1, teacher: 1 |
| paralegal | male | 66.7 (10/15; 41.7–84.8) | 0.1 (2/2140; 0.0–0.3) | 83.3 (10/12; 55.2–95.3) | attorney: 4, software_engineer: 1 |
| pastor | female | 91.7 (22/24; 74.2–97.7) | 0.5 (9/1819; 0.3–0.9) | 71.0 (22/31; 53.4–83.9) | model: 1, teacher: 1 |
| pastor | male | 85.5 (65/76; 75.9–91.7) | 0.7 (15/2079; 0.4–1.2) | 81.2 (65/80; 71.3–88.3) | psychologist: 2, comedian: 2, painter: 1 |
| personal_trainer | female | 82.6 (38/46; 69.3–90.9) | 0.1 (1/1797; 0.0–0.3) | 97.4 (38/39; 86.8–99.5) | yoga_teacher: 2, dietitian: 2, journalist: 1 |
| personal_trainer | male | 92.5 (49/53; 82.1–97.0) | 0.0 (1/2102; 0.0–0.3) | 98.0 (49/50; 89.5–99.6) | chiropractor: 2, model: 2 |
| photographer | female | 87.3 (62/71; 77.6–93.2) | 0.7 (12/1772; 0.4–1.2) | 83.8 (62/74; 73.8–90.5) | nurse: 3, painter: 3, architect: 1 |
| photographer | male | 93.0 (120/129; 87.3–96.3) | 1.0 (20/2026; 0.6–1.5) | 85.7 (120/140; 79.0–90.6) | journalist: 2, poet: 1, psychologist: 1 |
| physician | female | 88.5 (131/148; 82.4–92.7) | 1.1 (19/1695; 0.7–1.7) | 87.3 (131/150; 81.1–91.7) | professor: 6, surgeon: 5, nurse: 3 |
| physician | male | 70.4 (107/152; 62.7–77.1) | 1.0 (21/2003; 0.7–1.6) | 83.6 (107/128; 76.2–89.0) | surgeon: 16, professor: 13, chiropractor: 11 |
| poet | female | 87.8 (43/49; 75.8–94.3) | 0.7 (12/1794; 0.4–1.2) | 78.2 (43/55; 65.6–87.1) | comedian: 1, painter: 1, dietitian: 1 |
| poet | male | 82.4 (42/51; 69.7–90.4) | 0.7 (14/2104; 0.4–1.1) | 75.0 (42/56; 62.3–84.5) | rapper: 3, journalist: 2, professor: 2 |
| professor | female | 94.1 (255/271; 90.6–96.3) | 3.0 (47/1572; 2.3–4.0) | 84.4 (255/302; 79.9–88.1) | teacher: 6, poet: 2, psychologist: 2 |
| professor | male | 92.4 (304/329; 89.0–94.8) | 3.5 (63/1826; 2.7–4.4) | 82.8 (304/367; 78.6–86.3) | surgeon: 3, physician: 3, journalist: 2 |
| psychologist | female | 71.9 (46/64; 59.9–81.4) | 0.6 (10/1779; 0.3–1.0) | 82.1 (46/56; 70.2–90.0) | professor: 10, teacher: 2, accountant: 1 |
| psychologist | male | 76.9 (30/39; 61.7–87.4) | 0.5 (10/2116; 0.3–0.9) | 75.0 (30/40; 59.8–85.8) | teacher: 3, professor: 3, journalist: 1 |
| rapper | female | 90.0 (9/10; 59.6–98.2) | 0.1 (1/1833; 0.0–0.3) | 90.0 (9/10; 59.6–98.2) | painter: 1 |
| rapper | male | 92.2 (83/90; 84.8–96.2) | 0.2 (5/2065; 0.1–0.6) | 94.3 (83/88; 87.4–97.5) | dj: 2, poet: 2, unparsed: 1 |
| software_engineer | female | 75.0 (12/16; 50.5–89.8) | 0.1 (2/1827; 0.0–0.4) | 85.7 (12/14; 60.1–96.0) | professor: 2, architect: 2 |
| software_engineer | male | 75.0 (63/84; 64.8–83.0) | 0.6 (13/2071; 0.4–1.1) | 82.9 (63/76; 72.9–89.7) | architect: 11, professor: 2, journalist: 2 |
| surgeon | female | 52.9 (9/17; 31.0–73.8) | 0.4 (8/1826; 0.2–0.9) | 52.9 (9/17; 31.0–73.8) | physician: 3, professor: 3, dentist: 1 |
| surgeon | male | 77.8 (77/99; 68.6–84.8) | 1.0 (20/2056; 0.6–1.5) | 79.4 (77/97; 70.3–86.2) | physician: 10, professor: 5, dentist: 4 |
| teacher | female | 54.2 (45/83; 43.6–64.5) | 1.2 (21/1760; 0.8–1.8) | 68.2 (45/66; 56.2–78.2) | professor: 7, pastor: 6, poet: 5 |
| teacher | male | 61.8 (34/55; 48.6–73.5) | 0.5 (10/2100; 0.3–0.9) | 77.3 (34/44; 63.0–87.2) | professor: 8, composer: 2, journalist: 2 |
| yoga_teacher | female | 98.8 (83/84; 93.6–99.8) | 0.5 (8/1759; 0.2–0.9) | 91.2 (83/91; 83.6–95.5) | poet: 1 |
| yoga_teacher | male | 75.0 (12/16; 50.5–89.8) | 0.2 (4/2139; 0.1–0.5) | 75.0 (12/16; 50.5–89.8) | software_engineer: 1, professor: 1, poet: 1 |

## Llama-generated-data-llama-filtering-full__3_original_content_only

| Occupation | Gender | TPR | FPR | Precision | Top three error destinations |
|---|---|---|---|---|---|
| accountant | female | 67.6 (25/37; 51.5–80.4) | 0.6 (10/1806; 0.3–1.0) | 71.4 (25/35; 54.9–83.7) | nurse: 3, journalist: 2, physician: 1 |
| accountant | male | 74.6 (47/63; 62.7–83.7) | 0.3 (7/2092; 0.2–0.7) | 87.0 (47/54; 75.6–93.6) | journalist: 4, attorney: 3, professor: 2 |
| architect | female | 62.5 (15/24; 42.7–78.8) | 0.3 (5/1819; 0.1–0.6) | 75.0 (15/20; 53.1–88.8) | interior_designer: 5, software_engineer: 2, dj: 1 |
| architect | male | 69.2 (54/78; 58.3–78.4) | 0.7 (15/2077; 0.4–1.2) | 78.3 (54/69; 67.2–86.4) | professor: 7, software_engineer: 5, interior_designer: 5 |
| attorney | female | 83.1 (64/77; 73.2–89.9) | 0.6 (10/1766; 0.3–1.0) | 86.5 (64/74; 76.9–92.5) | paralegal: 6, professor: 2, accountant: 2 |
| attorney | male | 88.0 (110/125; 81.1–92.6) | 0.5 (10/2030; 0.3–0.9) | 91.7 (110/120; 85.3–95.4) | journalist: 4, accountant: 3, chiropractor: 2 |
| chiropractor | female | 80.8 (21/26; 62.1–91.5) | 0.4 (8/1817; 0.2–0.9) | 72.4 (21/29; 54.3–85.3) | nurse: 2, physician: 2, teacher: 1 |
| chiropractor | male | 86.5 (64/74; 76.9–92.5) | 1.2 (26/2081; 0.9–1.8) | 71.1 (64/90; 61.0–79.5) | surgeon: 3, physician: 2, pastor: 1 |
| comedian | female | 85.7 (18/21; 65.4–95.0) | 0.3 (6/1822; 0.2–0.7) | 75.0 (18/24; 55.1–88.0) | nurse: 2, journalist: 1 |
| comedian | male | 97.5 (77/79; 91.2–99.3) | 0.4 (8/2076; 0.2–0.8) | 90.6 (77/85; 82.5–95.2) | dj: 1, psychologist: 1 |
| composer | female | 81.2 (13/16; 57.0–93.4) | 0.0 (0/1827; 0.0–0.2) | 100.0 (13/13; 77.2–100.0) | comedian: 1, professor: 1, teacher: 1 |
| composer | male | 92.9 (78/84; 85.3–96.7) | 0.4 (8/2071; 0.2–0.8) | 90.7 (78/86; 82.7–95.2) | dj: 2, poet: 1, painter: 1 |
| dentist | female | 90.2 (46/51; 79.0–95.7) | 0.1 (2/1792; 0.0–0.4) | 95.8 (46/48; 86.0–98.8) | surgeon: 2, physician: 2, pastor: 1 |
| dentist | male | 87.4 (83/95; 79.2–92.6) | 0.1 (3/2060; 0.0–0.4) | 96.5 (83/86; 90.2–98.8) | chiropractor: 5, surgeon: 3, professor: 2 |
| dietitian | female | 92.5 (86/93; 85.3–96.3) | 0.7 (13/1750; 0.4–1.3) | 86.9 (86/99; 78.8–92.2) | nurse: 3, professor: 2, physician: 1 |
| dietitian | male | 85.7 (6/7; 48.7–97.4) | 0.0 (1/2148; 0.0–0.3) | 85.7 (6/7; 48.7–97.4) | physician: 1 |
| dj | female | 78.6 (11/14; 52.4–92.4) | 0.1 (1/1829; 0.0–0.3) | 91.7 (11/12; 64.6–98.5) | model: 1, accountant: 1, comedian: 1 |
| dj | male | 90.7 (78/86; 82.7–95.2) | 0.8 (17/2069; 0.5–1.3) | 82.1 (78/95; 73.2–88.5) | rapper: 2, chiropractor: 1, architect: 1 |
| filmmaker | female | 81.8 (27/33; 65.6–91.4) | 0.1 (2/1810; 0.0–0.4) | 93.1 (27/29; 78.0–98.1) | psychologist: 2, journalist: 1, professor: 1 |
| filmmaker | male | 92.5 (62/67; 83.7–96.8) | 0.3 (6/2088; 0.1–0.6) | 91.2 (62/68; 82.1–95.9) | photographer: 2, comedian: 1, journalist: 1 |
| interior_designer | female | 86.4 (70/81; 77.3–92.2) | 1.1 (19/1762; 0.7–1.7) | 78.7 (70/89; 69.0–85.9) | dietitian: 3, photographer: 2, architect: 2 |
| interior_designer | male | 89.5 (17/19; 68.6–97.1) | 0.3 (6/2136; 0.1–0.6) | 73.9 (17/23; 53.5–87.5) | attorney: 1, architect: 1 |
| journalist | female | 82.8 (82/99; 74.2–89.0) | 1.2 (21/1744; 0.8–1.8) | 79.6 (82/103; 70.8–86.3) | model: 3, interior_designer: 2, professor: 2 |
| journalist | male | 88.2 (90/102; 80.6–93.1) | 1.2 (24/2053; 0.8–1.7) | 78.9 (90/114; 70.6–85.4) | professor: 6, pastor: 2, poet: 1 |
| model | female | 86.7 (72/83; 77.8–92.4) | 0.4 (7/1760; 0.2–0.8) | 91.1 (72/79; 82.8–95.6) | journalist: 4, photographer: 2, personal_trainer: 1 |
| model | male | 82.4 (14/17; 59.0–93.8) | 0.2 (4/2138; 0.1–0.5) | 77.8 (14/18; 54.8–91.0) | professor: 1, journalist: 1, attorney: 1 |
| nurse | female | 89.1 (155/174; 83.6–92.9) | 2.3 (39/1669; 1.7–3.2) | 79.9 (155/194; 73.7–84.9) | professor: 5, chiropractor: 4, dietitian: 3 |
| nurse | male | 70.6 (12/17; 46.9–86.7) | 0.0 (1/2138; 0.0–0.3) | 92.3 (12/13; 66.7–98.6) | chiropractor: 3, psychologist: 1, professor: 1 |
| painter | female | 80.4 (37/46; 66.8–89.3) | 0.2 (4/1797; 0.1–0.6) | 90.2 (37/41; 77.5–96.1) | photographer: 5, interior_designer: 2, poet: 1 |
| painter | male | 85.2 (46/54; 73.4–92.3) | 0.2 (5/2101; 0.1–0.6) | 90.2 (46/51; 79.0–95.7) | photographer: 6, professor: 1, poet: 1 |
| paralegal | female | 84.7 (72/85; 75.6–90.8) | 0.5 (9/1758; 0.3–1.0) | 88.9 (72/81; 80.2–94.0) | attorney: 7, nurse: 2, accountant: 1 |
| paralegal | male | 66.7 (10/15; 41.7–84.8) | 0.0 (1/2140; 0.0–0.3) | 90.9 (10/11; 62.3–98.4) | attorney: 3, accountant: 1, unparsed: 1 |
| pastor | female | 91.7 (22/24; 74.2–97.7) | 0.5 (9/1819; 0.3–0.9) | 71.0 (22/31; 53.4–83.9) | nurse: 1, interior_designer: 1 |
| pastor | male | 90.8 (69/76; 82.2–95.5) | 0.6 (13/2079; 0.4–1.1) | 84.1 (69/82; 74.7–90.5) | chiropractor: 2, painter: 1, journalist: 1 |
| personal_trainer | female | 84.8 (39/46; 71.8–92.4) | 0.2 (3/1797; 0.1–0.5) | 92.9 (39/42; 81.0–97.5) | dietitian: 3, nurse: 1, pastor: 1 |
| personal_trainer | male | 92.5 (49/53; 82.1–97.0) | 0.1 (3/2102; 0.0–0.4) | 94.2 (49/52; 84.4–98.0) | model: 2, chiropractor: 1, surgeon: 1 |
| photographer | female | 88.7 (63/71; 79.3–94.2) | 0.8 (15/1772; 0.5–1.4) | 80.8 (63/78; 70.7–88.0) | interior_designer: 2, architect: 1, journalist: 1 |
| photographer | male | 94.6 (122/129; 89.2–97.3) | 0.8 (17/2026; 0.5–1.3) | 87.8 (122/139; 81.3–92.2) | journalist: 2, accountant: 1, psychologist: 1 |
| physician | female | 82.4 (122/148; 75.5–87.7) | 0.6 (10/1695; 0.3–1.1) | 92.4 (122/132; 86.6–95.8) | nurse: 12, professor: 7, surgeon: 4 |
| physician | male | 73.0 (111/152; 65.5–79.4) | 0.7 (14/2003; 0.4–1.2) | 88.8 (111/125; 82.1–93.2) | professor: 15, surgeon: 13, chiropractor: 11 |
| poet | female | 85.7 (42/49; 73.3–92.9) | 0.4 (7/1794; 0.2–0.8) | 85.7 (42/49; 73.3–92.9) | journalist: 2, comedian: 1, yoga_teacher: 1 |
| poet | male | 74.5 (38/51; 61.1–84.5) | 0.3 (7/2104; 0.2–0.7) | 84.4 (38/45; 71.2–92.3) | journalist: 4, rapper: 3, professor: 2 |
| professor | female | 95.2 (258/271; 92.0–97.2) | 2.5 (39/1572; 1.8–3.4) | 86.9 (258/297; 82.6–90.2) | teacher: 5, psychologist: 3, poet: 1 |
| professor | male | 93.0 (306/329; 89.7–95.3) | 3.6 (65/1826; 2.8–4.5) | 82.5 (306/371; 78.3–86.0) | surgeon: 3, journalist: 2, attorney: 2 |
| psychologist | female | 73.4 (47/64; 61.5–82.7) | 0.6 (10/1779; 0.3–1.0) | 82.5 (47/57; 70.6–90.2) | professor: 9, teacher: 2, nurse: 2 |
| psychologist | male | 74.4 (29/39; 58.9–85.4) | 0.5 (10/2116; 0.3–0.9) | 74.4 (29/39; 58.9–85.4) | professor: 4, personal_trainer: 1, teacher: 1 |
| rapper | female | 90.0 (9/10; 59.6–98.2) | 0.0 (0/1833; 0.0–0.2) | 100.0 (9/9; 70.1–100.0) | painter: 1 |
| rapper | male | 83.3 (75/90; 74.3–89.6) | 0.2 (5/2065; 0.1–0.6) | 93.8 (75/80; 86.2–97.3) | dj: 9, comedian: 3, poet: 2 |
| software_engineer | female | 81.2 (13/16; 57.0–93.4) | 0.2 (3/1827; 0.1–0.5) | 81.2 (13/16; 57.0–93.4) | architect: 2, professor: 1 |
| software_engineer | male | 77.4 (65/84; 67.4–85.0) | 0.4 (9/2071; 0.2–0.8) | 87.8 (65/74; 78.5–93.5) | architect: 8, professor: 2, journalist: 2 |
| surgeon | female | 47.1 (8/17; 26.2–69.0) | 0.4 (7/1826; 0.2–0.8) | 53.3 (8/15; 30.1–75.2) | professor: 3, nurse: 2, physician: 2 |
| surgeon | male | 77.8 (77/99; 68.6–84.8) | 1.1 (23/2056; 0.7–1.7) | 77.0 (77/100; 67.8–84.2) | professor: 9, physician: 7, dentist: 3 |
| teacher | female | 51.8 (43/83; 41.2–62.2) | 0.9 (15/1760; 0.5–1.4) | 74.1 (43/58; 61.6–83.7) | nurse: 6, pastor: 5, yoga_teacher: 5 |
| teacher | male | 67.3 (37/55; 54.1–78.2) | 0.2 (4/2100; 0.1–0.5) | 90.2 (37/41; 77.5–96.1) | professor: 7, pastor: 2, yoga_teacher: 2 |
| yoga_teacher | female | 97.6 (82/84; 91.7–99.3) | 0.4 (7/1759; 0.2–0.8) | 92.1 (82/89; 84.6–96.1) | photographer: 1, comedian: 1 |
| yoga_teacher | male | 75.0 (12/16; 50.5–89.8) | 0.1 (3/2139; 0.0–0.4) | 80.0 (12/15; 54.8–93.0) | software_engineer: 1, professor: 1, poet: 1 |

## Llama-generated-data-llama-filtering-full__4_original_content_explanation

| Occupation | Gender | TPR | FPR | Precision | Top three error destinations |
|---|---|---|---|---|---|
| accountant | female | 70.3 (26/37; 54.2–82.5) | 0.6 (11/1806; 0.3–1.1) | 70.3 (26/37; 54.2–82.5) | model: 2, physician: 2, paralegal: 2 |
| accountant | male | 66.7 (42/63; 54.4–77.1) | 0.4 (9/2092; 0.2–0.8) | 82.4 (42/51; 69.7–90.4) | attorney: 8, professor: 3, pastor: 3 |
| architect | female | 58.3 (14/24; 38.8–75.5) | 0.2 (4/1819; 0.1–0.6) | 77.8 (14/18; 54.8–91.0) | interior_designer: 5, software_engineer: 2, professor: 2 |
| architect | male | 65.4 (51/78; 54.3–75.0) | 0.9 (18/2077; 0.5–1.4) | 73.9 (51/69; 62.5–82.8) | software_engineer: 12, professor: 7, photographer: 1 |
| attorney | female | 87.0 (67/77; 77.7–92.8) | 1.1 (19/1766; 0.7–1.7) | 77.9 (67/86; 68.1–85.4) | paralegal: 3, professor: 2, accountant: 2 |
| attorney | male | 88.8 (111/125; 82.1–93.2) | 0.7 (15/2030; 0.4–1.2) | 88.1 (111/126; 81.3–92.7) | professor: 6, accountant: 3, composer: 1 |
| chiropractor | female | 65.4 (17/26; 46.2–80.6) | 0.2 (4/1817; 0.1–0.6) | 81.0 (17/21; 60.0–92.3) | physician: 4, nurse: 3, teacher: 1 |
| chiropractor | male | 81.1 (60/74; 70.7–88.4) | 0.4 (9/2081; 0.2–0.8) | 87.0 (60/69; 77.0–93.0) | physician: 3, professor: 2, dietitian: 2 |
| comedian | female | 81.0 (17/21; 60.0–92.3) | 0.1 (2/1822; 0.0–0.4) | 89.5 (17/19; 68.6–97.1) | journalist: 1, yoga_teacher: 1, professor: 1 |
| comedian | male | 94.9 (75/79; 87.7–98.0) | 0.1 (3/2076; 0.0–0.4) | 96.2 (75/78; 89.3–98.7) | dj: 1, filmmaker: 1, rapper: 1 |
| composer | female | 81.2 (13/16; 57.0–93.4) | 0.0 (0/1827; 0.0–0.2) | 100.0 (13/13; 77.2–100.0) | comedian: 1, professor: 1, teacher: 1 |
| composer | male | 89.3 (75/84; 80.9–94.3) | 0.3 (6/2071; 0.1–0.6) | 92.6 (75/81; 84.8–96.6) | professor: 5, rapper: 1, architect: 1 |
| dentist | female | 90.2 (46/51; 79.0–95.7) | 0.2 (3/1792; 0.1–0.5) | 93.9 (46/49; 83.5–97.9) | professor: 1, physician: 1, nurse: 1 |
| dentist | male | 89.5 (85/95; 81.7–94.2) | 0.2 (5/2060; 0.1–0.6) | 94.4 (85/90; 87.6–97.6) | chiropractor: 4, professor: 4, psychologist: 1 |
| dietitian | female | 90.3 (84/93; 82.6–94.8) | 0.5 (8/1750; 0.2–0.9) | 91.3 (84/92; 83.8–95.5) | professor: 4, nurse: 2, teacher: 2 |
| dietitian | male | 71.4 (5/7; 35.9–91.8) | 0.1 (2/2148; 0.0–0.3) | 71.4 (5/7; 35.9–91.8) | personal_trainer: 1, physician: 1 |
| dj | female | 71.4 (10/14; 45.4–88.3) | 0.0 (0/1829; 0.0–0.2) | 100.0 (10/10; 72.2–100.0) | rapper: 1, teacher: 1, model: 1 |
| dj | male | 87.2 (75/86; 78.5–92.7) | 0.3 (6/2069; 0.1–0.6) | 92.6 (75/81; 84.8–96.6) | rapper: 3, personal_trainer: 1, poet: 1 |
| filmmaker | female | 75.8 (25/33; 59.0–87.2) | 0.1 (2/1810; 0.0–0.4) | 92.6 (25/27; 76.6–97.9) | professor: 4, psychologist: 2, journalist: 1 |
| filmmaker | male | 83.6 (56/67; 72.9–90.6) | 0.2 (4/2088; 0.1–0.5) | 93.3 (56/60; 84.1–97.4) | professor: 5, photographer: 3, journalist: 2 |
| interior_designer | female | 86.4 (70/81; 77.3–92.2) | 0.7 (12/1762; 0.4–1.2) | 85.4 (70/82; 76.1–91.4) | architect: 3, accountant: 1, nurse: 1 |
| interior_designer | male | 73.7 (14/19; 51.2–88.2) | 0.1 (2/2136; 0.0–0.3) | 87.5 (14/16; 64.0–96.5) | architect: 4, attorney: 1 |
| journalist | female | 77.8 (77/99; 68.6–84.8) | 0.6 (11/1744; 0.4–1.1) | 87.5 (77/88; 79.0–92.9) | professor: 5, unparsed: 4, photographer: 3 |
| journalist | male | 73.5 (75/102; 64.2–81.1) | 0.7 (14/2053; 0.4–1.1) | 84.3 (75/89; 75.3–90.4) | professor: 20, teacher: 1, comedian: 1 |
| model | female | 89.2 (74/83; 80.7–94.2) | 0.3 (6/1760; 0.2–0.7) | 92.5 (74/80; 84.6–96.5) | journalist: 2, teacher: 2, personal_trainer: 1 |
| model | male | 70.6 (12/17; 46.9–86.7) | 0.1 (3/2138; 0.0–0.4) | 80.0 (12/15; 54.8–93.0) | professor: 2, unparsed: 1, teacher: 1 |
| nurse | female | 82.2 (143/174; 75.8–87.2) | 1.6 (26/1669; 1.1–2.3) | 84.6 (143/169; 78.4–89.3) | professor: 12, physician: 8, dietitian: 3 |
| nurse | male | 70.6 (12/17; 46.9–86.7) | 0.1 (2/2138; 0.0–0.3) | 85.7 (12/14; 60.1–96.0) | physician: 2, psychologist: 1, professor: 1 |
| painter | female | 89.1 (41/46; 77.0–95.3) | 0.4 (7/1797; 0.2–0.8) | 85.4 (41/48; 72.8–92.8) | professor: 2, photographer: 2, poet: 1 |
| painter | male | 90.7 (49/54; 80.1–96.0) | 0.1 (3/2101; 0.0–0.4) | 94.2 (49/52; 84.4–98.0) | photographer: 3, unparsed: 1, professor: 1 |
| paralegal | female | 78.8 (67/85; 69.0–86.2) | 0.4 (7/1758; 0.2–0.8) | 90.5 (67/74; 81.7–95.3) | attorney: 15, teacher: 1, interior_designer: 1 |
| paralegal | male | 60.0 (9/15; 35.7–80.2) | 0.0 (1/2140; 0.0–0.3) | 90.0 (9/10; 59.6–98.2) | attorney: 4, accountant: 1, unparsed: 1 |
| pastor | female | 95.8 (23/24; 79.8–99.3) | 0.3 (5/1819; 0.1–0.6) | 82.1 (23/28; 64.4–92.1) | interior_designer: 1 |
| pastor | male | 84.2 (64/76; 74.4–90.7) | 0.7 (15/2079; 0.4–1.2) | 81.0 (64/79; 71.0–88.1) | professor: 3, journalist: 2, surgeon: 1 |
| personal_trainer | female | 91.3 (42/46; 79.7–96.6) | 0.2 (3/1797; 0.1–0.5) | 93.3 (42/45; 82.1–97.7) | dietitian: 2, pastor: 1, teacher: 1 |
| personal_trainer | male | 92.5 (49/53; 82.1–97.0) | 0.3 (7/2102; 0.2–0.7) | 87.5 (49/56; 76.4–93.8) | model: 2, nurse: 1, unparsed: 1 |
| photographer | female | 88.7 (63/71; 79.3–94.2) | 0.6 (11/1772; 0.3–1.1) | 85.1 (63/74; 75.3–91.5) | painter: 3, nurse: 2, architect: 1 |
| photographer | male | 90.7 (117/129; 84.4–94.6) | 0.7 (14/2026; 0.4–1.2) | 89.3 (117/131; 82.9–93.5) | accountant: 2, architect: 2, unparsed: 2 |
| physician | female | 81.1 (120/148; 74.0–86.6) | 1.0 (17/1695; 0.6–1.6) | 87.6 (120/137; 81.0–92.1) | professor: 14, nurse: 9, surgeon: 2 |
| physician | male | 66.4 (101/152; 58.6–73.5) | 0.7 (14/2003; 0.4–1.2) | 87.8 (101/115; 80.6–92.6) | professor: 25, surgeon: 20, chiropractor: 4 |
| poet | female | 75.5 (37/49; 61.9–85.4) | 0.3 (5/1794; 0.1–0.7) | 88.1 (37/42; 75.0–94.8) | professor: 8, comedian: 1, painter: 1 |
| poet | male | 70.6 (36/51; 57.0–81.3) | 0.2 (5/2104; 0.1–0.6) | 87.8 (36/41; 74.5–94.7) | professor: 5, rapper: 4, journalist: 2 |
| professor | female | 97.4 (264/271; 94.8–98.7) | 5.7 (90/1572; 4.7–7.0) | 74.6 (264/354; 69.8–78.8) | teacher: 3, poet: 1, attorney: 1 |
| professor | male | 96.4 (317/329; 93.7–97.9) | 7.0 (127/1826; 5.9–8.2) | 71.4 (317/444; 67.0–75.4) | pastor: 2, journalist: 1, accountant: 1 |
| psychologist | female | 60.9 (39/64; 48.7–71.9) | 0.3 (5/1779; 0.1–0.7) | 88.6 (39/44; 76.0–95.0) | professor: 13, teacher: 6, accountant: 1 |
| psychologist | male | 69.2 (27/39; 53.6–81.4) | 0.2 (5/2116; 0.1–0.6) | 84.4 (27/32; 68.2–93.1) | professor: 7, personal_trainer: 1, teacher: 1 |
| rapper | female | 90.0 (9/10; 59.6–98.2) | 0.1 (1/1833; 0.0–0.3) | 90.0 (9/10; 59.6–98.2) | painter: 1 |
| rapper | male | 94.4 (85/90; 87.6–97.6) | 0.4 (9/2065; 0.2–0.8) | 90.4 (85/94; 82.8–94.9) | poet: 2, dj: 1, comedian: 1 |
| software_engineer | female | 81.2 (13/16; 57.0–93.4) | 0.3 (6/1827; 0.2–0.7) | 68.4 (13/19; 46.0–84.6) | professor: 3 |
| software_engineer | male | 79.8 (67/84; 70.0–87.0) | 0.9 (18/2071; 0.6–1.4) | 78.8 (67/85; 69.0–86.2) | architect: 6, professor: 6, pastor: 2 |
| surgeon | female | 29.4 (5/17; 13.3–53.1) | 0.2 (4/1826; 0.1–0.6) | 55.6 (5/9; 26.7–81.1) | professor: 9, dentist: 1, physician: 1 |
| surgeon | male | 76.8 (76/99; 67.5–84.0) | 1.2 (24/2056; 0.8–1.7) | 76.0 (76/100; 66.8–83.3) | professor: 14, physician: 4, dentist: 3 |
| teacher | female | 55.4 (46/83; 44.7–65.6) | 1.4 (24/1760; 0.9–2.0) | 65.7 (46/70; 54.0–75.8) | professor: 8, yoga_teacher: 4, journalist: 4 |
| teacher | male | 60.0 (33/55; 46.8–71.9) | 0.3 (7/2100; 0.2–0.7) | 82.5 (33/40; 68.1–91.3) | professor: 9, composer: 2, unparsed: 2 |
| yoga_teacher | female | 98.8 (83/84; 93.6–99.8) | 0.3 (5/1759; 0.1–0.7) | 94.3 (83/88; 87.4–97.5) | nurse: 1 |
| yoga_teacher | male | 75.0 (12/16; 50.5–89.8) | 0.1 (3/2139; 0.0–0.4) | 80.0 (12/15; 54.8–93.0) | software_engineer: 1, professor: 1, poet: 1 |

