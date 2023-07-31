import csv
import sqlite3
from datetime import datetime, timedelta
import requests
import json  # Import the json module
import difflib
import plotly.graph_objs as go
from plotly.subplots import make_subplots
from flask import Flask, render_template, request, redirect, url_for
from apscheduler.schedulers.background import BackgroundScheduler

app = Flask(__name__)

# Define the CSV file names for data storage
user_investment_csv = "user_investment.csv"
csv_file = "anime_scores.csv"

# Define a global variable to hold the current balance
balance = 10000  # Replace this value with the initial balance

anime_data_list = [
{
"id": 54595,
"title": "Kage no Jitsuryokusha ni Naritakute! 2nd Season",
"alternative_titles": {'synonyms': ['Shadow Garden 2nd Season'], 'en': 'The Eminence in Shadow Season 2', 'ja': '陰の実力者になりたくて！ 2nd Season', 'medium_picture': 'https://cdn.myanimelist.net/images/anime/1892/133677.jpg'},
"medium_picture": "https://cdn.myanimelist.net/images/anime/1892/133677.jpg"
},
{
"id": 51552,
"title": "Watashi no Shiawase na Kekkon",
"alternative_titles": {'synonyms': ['My Blissful Marriage'], 'en': 'My Happy Marriage', 'ja': 'わたしの幸せな結婚', 'medium_picture': 'https://cdn.myanimelist.net/images/anime/1147/122444.jpg'},
"medium_picture": "https://cdn.myanimelist.net/images/anime/1147/122444.jpg"
},
{
"id": 53716,
"title": "Hirogaru Sky! Precure",
"alternative_titles": {'synonyms': [], 'en': 'Soaring Sky! Pretty Cure', 'ja': 'ひろがるスカイ！プリキュア', 'medium_picture': 'https://cdn.myanimelist.net/images/anime/1762/135268.jpg'},
"medium_picture": "https://cdn.myanimelist.net/images/anime/1762/135268.jpg"
},
{
"id": 54898,
"title": "Bungou Stray Dogs 5th Season",
"alternative_titles": {'synonyms': [], 'en': 'Bungo Stray Dogs 5', 'ja': '文豪ストレイドッグス', 'medium_picture': 'https://cdn.myanimelist.net/images/anime/1161/136691.jpg'},
"medium_picture": "https://cdn.myanimelist.net/images/anime/1161/136691.jpg"
},
{
"id": 53127,
"title": "Fate/strange Fake: Whispers of Dawn",
"alternative_titles": {'synonyms': [], 'en': 'Fate/strange Fake: Whispers of Dawn', 'ja': 'Fate/strange Fake -Whispers of Dawn-', 'medium_picture': 'https://cdn.myanimelist.net/images/anime/1220/136619.jpg'},
"medium_picture": "https://cdn.myanimelist.net/images/anime/1220/136619.jpg"
},
{
"id": 49413,
"title": "Shiguang Dailiren II",
"alternative_titles": {'synonyms': ['Link Click 2nd Season'], 'en': 'Link Click Season 2', 'ja': '时光代理人 第二季', 'medium_picture': 'https://cdn.myanimelist.net/images/anime/1897/137108.jpg'},
"medium_picture": "https://cdn.myanimelist.net/images/anime/1897/137108.jpg"
},
{
"id": 53998,
"title": "Bleach: Sennen Kessen-hen - Ketsubetsu-tan",
"alternative_titles": {'synonyms': ['Bleach: Thousand-Year Blood War Arc'], 'en': 'Bleach: Thousand-Year Blood War - The Separation', 'ja': 'BLEACH 千年血戦篇-訣別譚-', 'medium_picture': 'https://cdn.myanimelist.net/images/anime/1018/136667.jpg'},
"medium_picture": "https://cdn.myanimelist.net/images/anime/1018/136667.jpg"
},
{
"id": 21,
"title": "One Piece",
"alternative_titles": {'synonyms': ['OP'], 'en': 'One Piece', 'ja': 'ONE PIECE', 'medium_picture': 'https://cdn.myanimelist.net/images/anime/6/73245.jpg'},
"medium_picture": "https://cdn.myanimelist.net/images/anime/6/73245.jpg"
},
{
"id": 54883,
"title": "Mononogatari 2nd Season",
"alternative_titles": {'synonyms': [], 'en': '', 'ja': 'もののがたり 第二章', 'medium_picture': 'https://cdn.myanimelist.net/images/anime/1111/135927.jpg'},
"medium_picture": "https://cdn.myanimelist.net/images/anime/1111/135927.jpg"
},
{
"id": 54842,
"title": "Sugar Apple Fairy Tale Part 2",
"alternative_titles": {'synonyms': [], 'en': '', 'ja': 'シュガーアップル・フェアリーテイル', 'medium_picture': 'https://cdn.myanimelist.net/images/anime/1399/136114.jpg'},
"medium_picture": "https://cdn.myanimelist.net/images/anime/1399/136114.jpg"
},
{
"id": 235,
"title": "Detective Conan",
"alternative_titles": {'synonyms': ['Meitantei Conan'], 'en': 'Case Closed', 'ja': '名探偵コナン', 'medium_picture': 'https://cdn.myanimelist.net/images/anime/7/75199.jpg'},
"medium_picture": "https://cdn.myanimelist.net/images/anime/7/75199.jpg"
},
{
"id": 51009,
"title": "Jujutsu Kaisen 2nd Season",
"alternative_titles": {'synonyms': ['Sorcery Fight', 'JJK'], 'en': '', 'ja': '呪術廻戦', 'medium_picture': 'https://cdn.myanimelist.net/images/anime/1600/134703.jpg'},
"medium_picture": "https://cdn.myanimelist.net/images/anime/1600/134703.jpg"
},
{
"id": 1199,
"title": "Nintama Rantarou",
"alternative_titles": {'synonyms': ['Ninja Boy Rantaro', 'Rakudaii Nintama Rantarou'], 'en': '', 'ja': '忍たま乱太郎', 'medium_picture': 'https://cdn.myanimelist.net/images/anime/6/74028.jpg'},
"medium_picture": "https://cdn.myanimelist.net/images/anime/6/74028.jpg"
},
{
"id": 36699,
"title": "Kimitachi wa Dou Ikiru ka",
"alternative_titles": {'synonyms': ['How Do You Live?'], 'en': 'The Boy and the Heron', 'ja': '君たちはどう生きるか', 'medium_picture': 'https://cdn.myanimelist.net/images/anime/1261/131805.jpg'},
"medium_picture": "https://cdn.myanimelist.net/images/anime/1261/131805.jpg"
},
{
"id": 23539,
"title": "Gudetama",
"alternative_titles": {'synonyms': [], 'en': 'The Lazy Egg', 'ja': 'ぐでたま', 'medium_picture': 'https://cdn.myanimelist.net/images/anime/10/79996.jpg'},
"medium_picture": "https://cdn.myanimelist.net/images/anime/10/79996.jpg"
},
{
"id": 50429,
"title": "Aiyou de Mishi",
"alternative_titles": {'synonyms': ["Aiyou's Secret Room"], 'en': 'X&Y', 'ja': '爱幽的密室', 'medium_picture': 'https://cdn.myanimelist.net/images/anime/1667/135309.jpg'},
"medium_picture": "https://cdn.myanimelist.net/images/anime/1667/135309.jpg"
},
{
"id": 8687,
"title": "Doraemon (2005)",
"alternative_titles": {'synonyms': [], 'en': '', 'ja': 'ドラえもん (2005)', 'medium_picture': 'https://cdn.myanimelist.net/images/anime/6/23935.jpg'},
"medium_picture": "https://cdn.myanimelist.net/images/anime/6/23935.jpg"
},
{
"id": 55651,
"title": "Tonikaku Kawaii: Joshikou-hen",
"alternative_titles": {'synonyms': ['Tonikaku Kawaii: High School Days'], 'en': 'TONIKAWA: Over The Moon For You - High School Days', 'ja': 'トニカクカワイイ 女子高編', 'medium_picture': 'https://cdn.myanimelist.net/images/anime/1922/136453.jpg'},
"medium_picture": "https://cdn.myanimelist.net/images/anime/1922/136453.jpg"
},
{
"id": 54856,
"title": "Horimiya: Piece",
"alternative_titles": {'synonyms': [], 'en': 'Horimiya: The Missing Pieces', 'ja': 'ホリミヤ -piece-', 'medium_picture': 'https://cdn.myanimelist.net/images/anime/1007/136277.jpg'},
"medium_picture": "https://cdn.myanimelist.net/images/anime/1007/136277.jpg"
},
{
"id": 54112,
"title": "Zom 100: Zombie ni Naru made ni Shitai 100 no Koto",
"alternative_titles": {'synonyms': ['Bucket List of The Dead, Zombie 100: 100 Things I Want to do Before I Become a Zombie'], 'en': 'Zom 100: Bucket List of the Dead', 'ja': 'ゾン100～ゾンビになるまでにしたい100のこと～', 'medium_picture': 'https://cdn.myanimelist.net/images/anime/1384/136408.jpg'},
"medium_picture": "https://cdn.myanimelist.net/images/anime/1384/136408.jpg"
},
{
"id": 52214,
"title": "Genjitsu no Yohane: Sunshine in the Mirror",
"alternative_titles": {'synonyms': [], 'en': 'Yohane the Parhelion: Sunshine in the Mirror', 'ja': '幻日のヨハネ -SUNSHINE in the MIRROR-', 'medium_picture': 'https://cdn.myanimelist.net/images/anime/1208/133335.jpg'},
"medium_picture": "https://cdn.myanimelist.net/images/anime/1208/133335.jpg"
},
{
"id": 53876,
"title": "Pokemon (2023)",
"alternative_titles": {'synonyms': ['Pokemon: Liko to Roy no Tabidachi', 'Pocket Monsters: Liko to Roy no Tabidachi', "Pokemon Horizons: Liko and Roy's Departure"], 'en': 'Pokémon Horizons: The Series', 'ja': 'ポケットモンスター(2023)', 'medium_picture': 'https://cdn.myanimelist.net/images/anime/1703/137216.jpg'},
"medium_picture": "https://cdn.myanimelist.net/images/anime/1703/137216.jpg"
},
{
"id": 53787,
"title": "AI no Idenshi",
"alternative_titles": {'synonyms': [], 'en': 'The Gene of AI', 'ja': 'AIの遺電子', 'medium_picture': 'https://cdn.myanimelist.net/images/anime/1706/136176.jpg'},
"medium_picture": "https://cdn.myanimelist.net/images/anime/1706/136176.jpg"
},
{
"id": 2406,
"title": "Sazae-san",
"alternative_titles": {'synonyms': [], 'en': 'Mrs. Sazae', 'ja': 'サザエさん', 'medium_picture': 'https://cdn.myanimelist.net/images/anime/1008/98996.jpg'},
"medium_picture": "https://cdn.myanimelist.net/images/anime/1008/98996.jpg"
},
{
"id": 53026,
"title": "Synduality: Noir",
"alternative_titles": {'synonyms': [], 'en': '', 'ja': 'SYNDUALITY Noir', 'medium_picture': 'https://cdn.myanimelist.net/images/anime/1464/134806.jpg'},
"medium_picture": "https://cdn.myanimelist.net/images/anime/1464/134806.jpg"
},
{
"id": 54398,
"title": "Biohazard: Death Island",
"alternative_titles": {'synonyms': [], 'en': 'Resident Evil: Death Island', 'ja': 'バイオハザード：デスアイランド', 'medium_picture': 'https://cdn.myanimelist.net/images/anime/1348/133200.jpg'},
"medium_picture": "https://cdn.myanimelist.net/images/anime/1348/133200.jpg"
},
{
"id": 54959,
"title": "BanG Dream! It's MyGO!!!!!",
"alternative_titles": {'synonyms': [], 'en': '', 'ja': "バンドリ！It's MyGO!!!!!", 'medium_picture': 'https://cdn.myanimelist.net/images/anime/1891/136948.jpg'},
"medium_picture": "https://cdn.myanimelist.net/images/anime/1891/136948.jpg"
},
{
"id": 55731,
"title": "Wu Nao Monu",
"alternative_titles": {'synonyms': ['Brainless Witch'], 'en': 'Agate', 'ja': '无脑魔女', 'medium_picture': 'https://cdn.myanimelist.net/images/anime/1386/136705.jpg'},
"medium_picture": "https://cdn.myanimelist.net/images/anime/1386/136705.jpg"
},
{
"id": 4459,
"title": "Ojarumaru",
"alternative_titles": {'synonyms': [], 'en': 'Prince Mackaroo', 'ja': 'おじゃる丸', 'medium_picture': 'https://cdn.myanimelist.net/images/anime/1839/132018.jpg'},
"medium_picture": "https://cdn.myanimelist.net/images/anime/1839/132018.jpg"
},
{
"id": 52079,
"title": "Cardfight!! Vanguard: will+Dress Season 3",
"alternative_titles": {'synonyms': ['Cardfight!! Vanguard: overDress'], 'en': '', 'ja': 'カードファイト!! ヴァンガード will+Dress Season3', 'medium_picture': 'https://cdn.myanimelist.net/images/anime/1739/136945.jpg'},
"medium_picture": "https://cdn.myanimelist.net/images/anime/1739/136945.jpg"
},
{
"id": 7505,
"title": "Knyacki!",
"alternative_titles": {'synonyms': [], 'en': '', 'ja': 'ニャッキ！', 'medium_picture': 'https://cdn.myanimelist.net/images/anime/2/55107.jpg'},
"medium_picture": "https://cdn.myanimelist.net/images/anime/2/55107.jpg"
},
{
"id": 54854,
"title": "Shadowverse Flame: Seven Shadows-hen",
"alternative_titles": {'synonyms': [], 'en': '', 'ja': 'シャドウバースF セブンシャドウズ編', 'medium_picture': 'https://cdn.myanimelist.net/images/anime/1070/134743.jpg'},
"medium_picture": "https://cdn.myanimelist.net/images/anime/1070/134743.jpg"
},
{
"id": 53426,
"title": "Hyakushou Kizoku",
"alternative_titles": {'synonyms': ['Noble Farmer'], 'en': '', 'ja': '百姓貴族', 'medium_picture': 'https://cdn.myanimelist.net/images/anime/1134/135615.jpg'},
"medium_picture": "https://cdn.myanimelist.net/images/anime/1134/135615.jpg"
},
{
"id": 32353,
"title": "Bonobono (TV 2016)",
"alternative_titles": {'synonyms': [], 'en': 'Bono Bono', 'ja': 'ぼのぼの', 'medium_picture': 'https://cdn.myanimelist.net/images/anime/13/77617.jpg'},
"medium_picture": "https://cdn.myanimelist.net/images/anime/13/77617.jpg"
},
{
"id": 56015,
"title": "Miraijima",
"alternative_titles": {'synonyms': [], 'en': 'Future Island', 'ja': '未来島 ~Future Island~', 'medium_picture': 'https://cdn.myanimelist.net/images/anime/1776/137220.jpg'},
"medium_picture": "https://cdn.myanimelist.net/images/anime/1776/137220.jpg"
},
{
"id": 52614,
"title": "Mix: Meisei Story 2nd Season - Nidome no Natsu, Sora no Mukou e",
"alternative_titles": {'synonyms': [], 'en': 'MIX Season 2', 'ja': 'MIX MEISEI STORY 2ND SEASON 〜二度目の夏、空の向こうへ〜', 'medium_picture': 'https://cdn.myanimelist.net/images/anime/1727/137215.jpg'},
"medium_picture": "https://cdn.myanimelist.net/images/anime/1727/137215.jpg"
},
{
"id": 6149,
"title": "Chibi Maruko-chan (1995)",
"alternative_titles": {'synonyms': ['Maruko-chan'], 'en': 'Little Miss Maruko', 'ja': 'ちびまる子ちゃん', 'medium_picture': 'https://cdn.myanimelist.net/images/anime/1108/100604.jpg'},
"medium_picture": "https://cdn.myanimelist.net/images/anime/1108/100604.jpg"
},
{
"id": 51458,
"title": "Lv1 Maou to One Room Yuusha",
"alternative_titles": {'synonyms': [], 'en': 'Level 1 Demon Lord and One Room Hero', 'ja': 'Lv1魔王とワンルーム勇者', 'medium_picture': 'https://cdn.myanimelist.net/images/anime/1879/136721.jpg'},
"medium_picture": "https://cdn.myanimelist.net/images/anime/1879/136721.jpg"
},
{
"id": 1960,
"title": "Sore Ike! Anpanman",
"alternative_titles": {'synonyms': ['Soreike! Anpanman', 'Go! Anpanman', 'Anpanman TV'], 'en': '', 'ja': 'それいけ！アンパンマン', 'medium_picture': 'https://cdn.myanimelist.net/images/anime/1902/111797.jpg'},
"medium_picture": "https://cdn.myanimelist.net/images/anime/1902/111797.jpg"
},
{
"id": 53859,
"title": "Wan Sheng Jie 4",
"alternative_titles": {'synonyms': ['All Saints Street 4'], 'en': 'All Saints Street 4', 'ja': '万圣街4', 'medium_picture': 'https://cdn.myanimelist.net/images/anime/1567/137044.jpg'},
"medium_picture": "https://cdn.myanimelist.net/images/anime/1567/137044.jpg"
},
{
"id": 54947,
"title": "Spy Kyoushitsu 2nd Season",
"alternative_titles": {'synonyms': ['Spy Room 2'], 'en': 'Spy Classroom Season 2', 'ja': 'スパイ教室', 'medium_picture': 'https://cdn.myanimelist.net/images/anime/1317/136666.jpg'},
"medium_picture": "https://cdn.myanimelist.net/images/anime/1317/136666.jpg"
},
{
"id": 48633,
"title": "Liar Liar",
"alternative_titles": {'synonyms': [], 'en': '', 'ja': 'ライアー・ライアー', 'medium_picture': 'https://cdn.myanimelist.net/images/anime/1571/134525.jpg'},
"medium_picture": "https://cdn.myanimelist.net/images/anime/1571/134525.jpg"
},
{
"id": 54790,
"title": "Undead Girl Murder Farce",
"alternative_titles": {'synonyms': [], 'en': 'Undead Murder Farce', 'ja': 'アンデッドガール・マーダーファルス', 'medium_picture': 'https://cdn.myanimelist.net/images/anime/1946/136661.jpg'},
"medium_picture": "https://cdn.myanimelist.net/images/anime/1946/136661.jpg"
},
{
"id": 49858,
"title": "Shinigami Bocchan to Kuro Maid 2nd Season",
"alternative_titles": {'synonyms': [], 'en': 'The Duke of Death and His Maid Season 2', 'ja': '死神坊ちゃんと黒メイド', 'medium_picture': 'https://cdn.myanimelist.net/images/anime/1078/136947.jpg'},
"medium_picture": "https://cdn.myanimelist.net/images/anime/1078/136947.jpg"
},
{
"id": 50002,
"title": "Edens Zero 2nd Season",
"alternative_titles": {'synonyms': [], 'en': '', 'ja': 'エデンズ ゼロ', 'medium_picture': 'https://cdn.myanimelist.net/images/anime/1872/137116.jpg'},
"medium_picture": "https://cdn.myanimelist.net/images/anime/1872/137116.jpg"
},
{
"id": 53050,
"title": "Kanojo, Okarishimasu 3rd Season",
"alternative_titles": {'synonyms': ['Kanokari'], 'en': 'Rent-a-Girlfriend Season 3', 'ja': '彼女、お借りします', 'medium_picture': 'https://cdn.myanimelist.net/images/anime/1696/136634.jpg'},
"medium_picture": "https://cdn.myanimelist.net/images/anime/1696/136634.jpg"
},
{
"id": 52505,
"title": "Dark Gathering",
"alternative_titles": {'synonyms': [], 'en': 'Dark Gathering', 'ja': 'ダークギャザリング', 'medium_picture': 'https://cdn.myanimelist.net/images/anime/1748/136736.jpg'},
"medium_picture": "https://cdn.myanimelist.net/images/anime/1748/136736.jpg"
},
{
"id": 53200,
"title": "Hataraku Maou-sama!! 2nd Season",
"alternative_titles": {'synonyms': ['The Devil is a Part-Timer! 3rd Season', 'Hataraku Maou-sama 3'], 'en': 'The Devil is a Part-Timer! Season 2 (Sequel)', 'ja': 'はたらく魔王さま！！', 'medium_picture': 'https://cdn.myanimelist.net/images/anime/1392/136670.jpg'},
"medium_picture": "https://cdn.myanimelist.net/images/anime/1392/136670.jpg"
},
{
"id": 50613,
"title": "Rurouni Kenshin: Meiji Kenkaku Romantan (2023)",
"alternative_titles": {'synonyms': [], 'en': '', 'ja': 'るろうに剣心 -明治剣客浪漫譚-', 'medium_picture': 'https://cdn.myanimelist.net/images/anime/1599/136532.jpg'},
"medium_picture": "https://cdn.myanimelist.net/images/anime/1599/136532.jpg"
},
{
"id": 966,
"title": "Crayon Shin-chan",
"alternative_titles": {'synonyms': [], 'en': 'Shin Chan', 'ja': 'クレヨンしんちゃん', 'medium_picture': 'https://cdn.myanimelist.net/images/anime/10/59897.jpg'},
"medium_picture": "https://cdn.myanimelist.net/images/anime/10/59897.jpg"
},
{
"id": 52969,
"title": "Jitsu wa Ore, Saikyou deshita?",
"alternative_titles": {'synonyms': [], 'en': 'Am I Actually the Strongest?', 'ja': '実は俺、最強でした?', 'medium_picture': 'https://cdn.myanimelist.net/images/anime/1496/136558.jpg'},
"medium_picture": "https://cdn.myanimelist.net/images/anime/1496/136558.jpg"
},
{
"id": 50582,
"title": "Nanatsu no Maken ga Shihai suru",
"alternative_titles": {'synonyms': ['Nanatsuma'], 'en': 'Reign of the Seven Spellblades', 'ja': '七つの魔剣が支配する', 'medium_picture': 'https://cdn.myanimelist.net/images/anime/1396/136273.jpg'},
"medium_picture": "https://cdn.myanimelist.net/images/anime/1396/136273.jpg"
},
{
"id": 54234,
"title": "Suki na Ko ga Megane wo Wasureta",
"alternative_titles": {'synonyms': [], 'en': 'The Girl I Like Forgot Her Glasses', 'ja': '好きな子がめがねを忘れた', 'medium_picture': 'https://cdn.myanimelist.net/images/anime/1582/136325.jpg'},
"medium_picture": "https://cdn.myanimelist.net/images/anime/1582/136325.jpg"
},
{
"id": 51020,
"title": "Helck",
"alternative_titles": {'synonyms': [], 'en': 'Helck', 'ja': 'ヘルク', 'medium_picture': 'https://cdn.myanimelist.net/images/anime/1879/133302.jpg'},
"medium_picture": "https://cdn.myanimelist.net/images/anime/1879/133302.jpg"
},
{
"id": 51498,
"title": "Masamune-kun no Revenge R",
"alternative_titles": {'synonyms': [], 'en': "Masamune-kun's Revenge R", 'ja': '政宗くんのリベンジR', 'medium_picture': 'https://cdn.myanimelist.net/images/anime/1667/135587.jpg'},
"medium_picture": "https://cdn.myanimelist.net/images/anime/1667/135587.jpg"
},
{
"id": 55826,
"title": "Seishun Archive",
"alternative_titles": {'synonyms': ['Hololive Summer 2023 MV'], 'en': 'Seishun Archive', 'ja': '青春アーカイブ', 'medium_picture': 'https://cdn.myanimelist.net/images/anime/1983/136831.jpg'},
"medium_picture": "https://cdn.myanimelist.net/images/anime/1983/136831.jpg"
},
{
"id": 53438,
"title": "Higeki no Genkyou to Naru Saikyou Gedou Last Boss Joou wa Tami no Tame ni Tsukushimasu.",
"alternative_titles": {'synonyms': ['The Most Heretical Last Boss Queen Who Will Become the Source of Tragedy Will Devote Herself for the Sake of the People', 'Lastame'], 'en': 'The Most Heretical Last Boss Queen: From Villainess to Savior', 'ja': '悲劇の元凶となる最強外道ラスボス女王は民の為に尽くします。', 'medium_picture': 'https://cdn.myanimelist.net/images/anime/1722/135542.jpg'},
"medium_picture": "https://cdn.myanimelist.net/images/anime/1722/135542.jpg"
},
{
"id": 54915,
"title": "5-toubun no Hanayome∽",
"alternative_titles": {'synonyms': [], 'en': 'The Quintessential Quintuplets~', 'ja': '五等分の花嫁∽', 'medium_picture': 'https://cdn.myanimelist.net/images/anime/1567/135752.jpg'},
"medium_picture": "https://cdn.myanimelist.net/images/anime/1567/135752.jpg"
},
{
"id": 52082,
"title": "Shiro Seijo to Kuro Bokushi",
"alternative_titles": {'synonyms': ['White Saint and Black Pastor'], 'en': 'Saint Cecilia and Pastor Lawrence', 'ja': '白聖女と黒牧師', 'medium_picture': 'https://cdn.myanimelist.net/images/anime/1329/135096.jpg'},
"medium_picture": "https://cdn.myanimelist.net/images/anime/1329/135096.jpg"
},
{
"id": 46422,
"title": "Niehime to Kemono no Ou",
"alternative_titles": {'synonyms': [], 'en': 'Sacrificial Princess and the King of Beasts', 'ja': '贄姫と獣の王', 'medium_picture': 'https://cdn.myanimelist.net/images/anime/1997/127227.jpg'},
"medium_picture": "https://cdn.myanimelist.net/images/anime/1997/127227.jpg"
},
{
"id": 51916,
"title": "Dekiru Neko wa Kyou mo Yuuutsu",
"alternative_titles": {'synonyms': ['Dekineko'], 'en': 'The Masterful Cat Is Depressed Again Today', 'ja': 'デキる猫は今日も憂鬱', 'medium_picture': 'https://cdn.myanimelist.net/images/anime/1074/136720.jpg'},
"medium_picture": "https://cdn.myanimelist.net/images/anime/1074/136720.jpg"
},
{
"id": 51614,
"title": "Ao no Orchestra",
"alternative_titles": {'synonyms': ['The Blue Orchestra'], 'en': 'Blue Orchestra', 'ja': '青のオーケストラ', 'medium_picture': 'https://cdn.myanimelist.net/images/anime/1832/133754.jpg'},
"medium_picture": "https://cdn.myanimelist.net/images/anime/1832/133754.jpg"
},
{
"id": 55166,
"title": "Yami Shibai 11",
"alternative_titles": {'synonyms': ['Yamishibai: Japanese Ghost Stories Eleventh Season, Yamishibai: Japanese Ghost Stories 11'], 'en': '', 'ja': '闇芝居 十一期', 'medium_picture': 'https://cdn.myanimelist.net/images/anime/1375/135625.jpg'},
"medium_picture": "https://cdn.myanimelist.net/images/anime/1375/135625.jpg"
},
{
"id": 8336,
"title": "Hanakappa",
"alternative_titles": {'synonyms': ['Hana Kappa'], 'en': '', 'ja': 'はなかっぱ', 'medium_picture': 'https://cdn.myanimelist.net/images/anime/1105/90503.jpg'},
"medium_picture": "https://cdn.myanimelist.net/images/anime/1105/90503.jpg"
},
{
"id": 48417,
"title": "Maou Gakuin no Futekigousha: Shijou Saikyou no Maou no Shiso, Tensei shite Shison-tachi no Gakkou e Kayou II",
"alternative_titles": {'synonyms': ['Maou Gakuin no Futekigousha: Shijou Saikyou no Maou no Shiso, Tensei shite Shison-tachi no Gakkou e Kayou 2nd Season', 'The Misfit of Demon King Academy 2nd Season'], 'en': 'The Misfit of Demon King Academy Ⅱ', 'ja': '魔王学院の不適合者 ～史上最強の魔王の始祖、転生して子孫たちの学校へ通う～ II', 'medium_picture': 'https://cdn.myanimelist.net/images/anime/1475/137152.jpg'},
"medium_picture": "https://cdn.myanimelist.net/images/anime/1475/137152.jpg"
},
{
"id": 50418,
"title": "Ninjala (TV)",
"alternative_titles": {'synonyms': [], 'en': '', 'ja': 'ニンジャラ', 'medium_picture': 'https://cdn.myanimelist.net/images/anime/1552/119871.jpg'},
"medium_picture": "https://cdn.myanimelist.net/images/anime/1552/119871.jpg"
},
{
"id": 50607,
"title": "Yu☆Gi☆Oh! Go Rush!!",
"alternative_titles": {'synonyms': ['Yuu Gi Ou: Go Rush!!'], 'en': '', 'ja': '遊☆戯☆王ゴーラッシュ!!', 'medium_picture': 'https://cdn.myanimelist.net/images/anime/1624/134752.jpg'},
"medium_picture": "https://cdn.myanimelist.net/images/anime/1624/134752.jpg"
},
{
"id": 42295,
"title": "Fushigi Dagashiya: Zenitendou",
"alternative_titles": {'synonyms': [], 'en': '', 'ja': 'ふしぎ駄菓子屋 銭天堂', 'medium_picture': 'https://cdn.myanimelist.net/images/anime/1994/108212.jpg'},
"medium_picture": "https://cdn.myanimelist.net/images/anime/1994/108212.jpg"
},
{
"id": 35694,
"title": "Kirin the Noop",
"alternative_titles": {'synonyms': [], 'en': 'Kirin the Noop', 'ja': 'キリン・ザ・ヌープ', 'medium_picture': 'https://cdn.myanimelist.net/images/anime/13/86110.jpg'},
"medium_picture": "https://cdn.myanimelist.net/images/anime/13/86110.jpg"
},
{
"id": 37096,
"title": "Puzzle & Dragon",
"alternative_titles": {'synonyms': ['PazuDora'], 'en': 'Puzzle & Dragon', 'ja': 'パズドラ', 'medium_picture': 'https://cdn.myanimelist.net/images/anime/1535/95070.jpg'},
"medium_picture": "https://cdn.myanimelist.net/images/anime/1535/95070.jpg"
},
{
"id": 55878,
"title": "Hataraku Maou-sama!! Recap",
"alternative_titles": {'synonyms': [], 'en': 'Recap Special From Sasazuka to Ente Isla!', 'ja': 'はたらく魔王さま！！', 'medium_picture': 'https://cdn.myanimelist.net/images/anime/1463/136983.jpg'},
"medium_picture": "https://cdn.myanimelist.net/images/anime/1463/136983.jpg"
},
{
"id": 53379,
"title": "Uchi no Kaisha no Chiisai Senpai no Hanashi",
"alternative_titles": {'synonyms': ["My Company's Small Senpai, Story of a Small Senior in My Company"], 'en': 'My Tiny Senpai', 'ja': 'うちの会社の小さい先輩の話', 'medium_picture': 'https://cdn.myanimelist.net/images/anime/1984/136274.jpg'},
"medium_picture": "https://cdn.myanimelist.net/images/anime/1984/136274.jpg"
},
{
"id": 51764,
"title": "Level 1 dakedo Unique Skill de Saikyou desu",
"alternative_titles": {'synonyms': [], 'en': 'My Unique Skill Makes Me OP Even at Level 1', 'ja': 'レベル1だけどユニークスキルで最強です', 'medium_picture': 'https://cdn.myanimelist.net/images/anime/1579/136295.jpg'},
"medium_picture": "https://cdn.myanimelist.net/images/anime/1579/136295.jpg"
},
{
"id": 54760,
"title": "Ryza no Atelier: Tokoyami no Joou to Himitsu no Kakurega",
"alternative_titles": {'synonyms': [], 'en': 'Atelier Ryza: Ever Darkness & the Secret Hideout The Animation', 'ja': 'ライザのアトリエ ~常闇の女王と秘密の隠れ家~', 'medium_picture': 'https://cdn.myanimelist.net/images/anime/1079/136949.jpg'},
"medium_picture": "https://cdn.myanimelist.net/images/anime/1079/136949.jpg"
},
{
"id": 52619,
"title": "Jidou Hanbaiki ni Umarekawatta Ore wa Meikyuu wo Samayou",
"alternative_titles": {'synonyms': ['I Was Reborn as a Vending Machine, Wandering in the Dungeon', 'I Reincarnated Into a Vending Machine'], 'en': 'Reborn as a Vending Machine, I Now Wander the Dungeon', 'ja': '自動販売機に生まれ変わった俺は迷宮を彷徨う', 'medium_picture': 'https://cdn.myanimelist.net/images/anime/1653/136097.jpg'},
"medium_picture": "https://cdn.myanimelist.net/images/anime/1653/136097.jpg"
},
{
"id": 53263,
"title": "Seija Musou: Salaryman, Isekai de Ikinokoru Tame ni Ayumu Michi",
"alternative_titles": {'synonyms': [], 'en': 'The Great Cleric', 'ja': '聖者無双', 'medium_picture': 'https://cdn.myanimelist.net/images/anime/1821/135926.jpg'},
"medium_picture": "https://cdn.myanimelist.net/images/anime/1821/135926.jpg"
},
{
"id": 52611,
"title": "Okashi na Tensei",
"alternative_titles": {'synonyms': ['Treat of Reincarnation'], 'en': 'Sweet Reincarnation', 'ja': 'おかしな転生', 'medium_picture': 'https://cdn.myanimelist.net/images/anime/1251/136232.jpg'},
"medium_picture": "https://cdn.myanimelist.net/images/anime/1251/136232.jpg"
},
{
"id": 53632,
"title": "Yumemiru Danshi wa Genjitsushugisha",
"alternative_titles": {'synonyms': [], 'en': 'The Dreaming Boy is a Realist', 'ja': '夢見る男子は現実主義者', 'medium_picture': 'https://cdn.myanimelist.net/images/anime/1239/134810.jpg'},
"medium_picture": "https://cdn.myanimelist.net/images/anime/1239/134810.jpg"
},
{
"id": 55020,
"title": "Go! Go! Vehicle Zoo",
"alternative_titles": {'synonyms': [], 'en': '', 'ja': 'ゴー！ゴ―！びーくるずー', 'medium_picture': 'https://cdn.myanimelist.net/images/anime/1601/135341.jpg'},
"medium_picture": "https://cdn.myanimelist.net/images/anime/1601/135341.jpg"
},
{
"id": 55693,
"title": "Zhen Yang Wushen",
"alternative_titles": {'synonyms': [], 'en': 'Soul of Light', 'ja': '真阳武神', 'medium_picture': 'https://cdn.myanimelist.net/images/anime/1769/136525.jpg'},
"medium_picture": "https://cdn.myanimelist.net/images/anime/1769/136525.jpg"
},
{
"id": 55195,
"title": "Mamekichi Mameko NEET no Nichijou 2nd Season",
"alternative_titles": {'synonyms': [], 'en': "Mameko Mamekichi's NEET Everyday Life 2nd Season", 'ja': 'まめきちまめこニートの日常', 'medium_picture': 'https://cdn.myanimelist.net/images/anime/1618/135681.jpg'},
"medium_picture": "https://cdn.myanimelist.net/images/anime/1618/135681.jpg"
},
{
"id": 55999,
"title": "Skysonar",
"alternative_titles": {'synonyms': [], 'en': '', 'ja': 'SKYSONAR', 'medium_picture': 'https://cdn.myanimelist.net/images/anime/1832/137180.jpg'},
"medium_picture": "https://cdn.myanimelist.net/images/anime/1832/137180.jpg"
},
{
"id": 38099,
"title": "Pakkororin",
"alternative_titles": {'synonyms': [], 'en': 'Pakkororin', 'ja': 'パッコロリン', 'medium_picture': 'https://cdn.myanimelist.net/images/anime/1134/93318.jpg'},
"medium_picture": "https://cdn.myanimelist.net/images/anime/1134/93318.jpg"
},
{
"id": 52066,
"title": "Recola",
"alternative_titles": {'synonyms': [], 'en': '', 'ja': 'リコラ', 'medium_picture': 'https://cdn.myanimelist.net/images/anime/1564/124424.jpg'},
"medium_picture": "https://cdn.myanimelist.net/images/anime/1564/124424.jpg"
},
{
"id": 55745,
"title": "Ni Tian Xieshen",
"alternative_titles": {'synonyms': [], 'en': '', 'ja': '逆天邪神', 'medium_picture': 'https://cdn.myanimelist.net/images/anime/1621/136623.jpg'},
"medium_picture": "https://cdn.myanimelist.net/images/anime/1621/136623.jpg"
},
{
"id": 54659,
"title": "Sore Shikanai Wakenai deshou",
"alternative_titles": {'synonyms': [], 'en': '', 'ja': 'それしか ないわけ ないでしょう', 'medium_picture': 'https://cdn.myanimelist.net/images/anime/1977/133957.jpg'},
"medium_picture": "https://cdn.myanimelist.net/images/anime/1977/133957.jpg"
},
{
"id": 55864,
"title": "Jiu Chen Fengyun Lu",
"alternative_titles": {'synonyms': [], 'en': '', 'ja': '九辰风云录', 'medium_picture': 'https://cdn.myanimelist.net/images/anime/1250/136941.jpg'},
"medium_picture": "https://cdn.myanimelist.net/images/anime/1250/136941.jpg"
},
{
"id": 55993,
"title": "Fanren Xiu Xian Chuan: Xinghai Feichi Pian Xuzhang",
"alternative_titles": {'synonyms': [], 'en': '', 'ja': '凡人修仙传 星海飞驰篇 序章', 'medium_picture': 'https://cdn.myanimelist.net/images/anime/1690/137149.jpg'},
"medium_picture": "https://cdn.myanimelist.net/images/anime/1690/137149.jpg"
},
{
"id": 55047,
"title": "Sinbi Apateu: Zero",
"alternative_titles": {'synonyms': [], 'en': '', 'ja': '신비아파트 고스트볼 ZERO', 'medium_picture': 'https://cdn.myanimelist.net/images/anime/1850/135377.jpg'},
"medium_picture": "https://cdn.myanimelist.net/images/anime/1850/135377.jpg"
},
{
"id": 51291,
"title": "Duo Xuan Shi",
"alternative_titles": {'synonyms': [], 'en': 'Fallen Mystic Master', 'ja': '堕玄师', 'medium_picture': 'https://cdn.myanimelist.net/images/anime/1090/126770.jpg'},
"medium_picture": "https://cdn.myanimelist.net/images/anime/1090/126770.jpg"
},
{
"id": 55738,
"title": "Guaishou Xiao Guan",
"alternative_titles": {'synonyms': [], 'en': 'Monster Diner', 'ja': '怪兽小馆', 'medium_picture': 'https://cdn.myanimelist.net/images/anime/1169/136606.jpg'},
"medium_picture": "https://cdn.myanimelist.net/images/anime/1169/136606.jpg"
},
{
"id": 52076,
"title": "Akikan no Tuna",
"alternative_titles": {'synonyms': [], 'en': '', 'ja': '空き缶のツナ', 'medium_picture': 'https://cdn.myanimelist.net/images/anime/1012/124452.jpg'},
"medium_picture": "https://cdn.myanimelist.net/images/anime/1012/124452.jpg"
},
{
"id": 55740,
"title": "Shen Lan Qi Yu Wushuang Zhu: Tianmo Pian - Ding Dang",
"alternative_titles": {'synonyms': [], 'en': 'The Land of Miracles 3rd Season', 'ja': '神澜奇域无双珠 天魔篇定档', 'medium_picture': 'https://cdn.myanimelist.net/images/anime/1200/136617.jpg'},
"medium_picture": "https://cdn.myanimelist.net/images/anime/1200/136617.jpg"
},
{
"id": 55463,
"title": "Odekake Kozame",
"alternative_titles": {'synonyms': ["Little Shark's Outings"], 'en': '', 'ja': 'おでかけ子ザメ', 'medium_picture': 'https://cdn.myanimelist.net/images/anime/1464/136707.jpg'},
"medium_picture": "https://cdn.myanimelist.net/images/anime/1464/136707.jpg"
},
{
"id": 53514,
"title": "Oshiri Tantei 7th Season",
"alternative_titles": {'synonyms': ['Butt Detective'], 'en': '', 'ja': 'おしりたんてい', 'medium_picture': 'https://cdn.myanimelist.net/images/anime/1288/130433.jpg'},
"medium_picture": "https://cdn.myanimelist.net/images/anime/1288/130433.jpg"
},
{
"id": 55829,
"title": "Shi Fang Jian Sheng",
"alternative_titles": {'synonyms': ['Shi Fang Shen Wang', '十方神王'], 'en': '', 'ja': '十方剑圣', 'medium_picture': 'https://cdn.myanimelist.net/images/anime/1936/136828.jpg'},
"medium_picture": "https://cdn.myanimelist.net/images/anime/1936/136828.jpg"
},
{
"id": 41458,
"title": "Origami Ninja Koyankinte",
"alternative_titles": {'synonyms': ['Happy Smile ♡ Dream'], 'en': '', 'ja': 'おりがみにんじゃ コーヤン＠きんてれ', 'medium_picture': 'https://cdn.myanimelist.net/images/anime/1860/106477.jpg'},
"medium_picture": "https://cdn.myanimelist.net/images/anime/1860/106477.jpg"
},
{
"id": 38451,
"title": "Reizouko no Tsukenosuke!",
"alternative_titles": {'synonyms': ['Reizouko no Tsuke no Suke!'], 'en': '', 'ja': 'れいぞうこのつけのすけ！', 'medium_picture': 'https://cdn.myanimelist.net/images/anime/1884/95217.jpg'},
"medium_picture": "https://cdn.myanimelist.net/images/anime/1884/95217.jpg"
},
{
"id": 55908,
"title": "Golden Ray",
"alternative_titles": {'synonyms': [], 'en': 'Golden Ray', 'ja': 'ゴールデンレイ', 'medium_picture': 'https://cdn.myanimelist.net/images/anime/1940/137034.jpg'},
"medium_picture": "https://cdn.myanimelist.net/images/anime/1940/137034.jpg"
},
{
"id": 55937,
"title": "Gangu",
"alternative_titles": {'synonyms': ['Omocha'], 'en': 'Toy', 'ja': '玩具', 'medium_picture': 'https://cdn.myanimelist.net/images/anime/1618/137077.jpg'},
"medium_picture": "https://cdn.myanimelist.net/images/anime/1618/137077.jpg"
},
{
"id": 34990,
"title": "Unicorn no Kyupi",
"alternative_titles": {'synonyms': [], 'en': '', 'ja': 'ユニコーンのキュピ', 'medium_picture': 'https://cdn.myanimelist.net/images/anime/1165/91319.jpg'},
"medium_picture": "https://cdn.myanimelist.net/images/anime/1165/91319.jpg"
},
{
"id": 56035,
"title": "Renjo Shiika",
"alternative_titles": {'synonyms': [], 'en': '', 'ja': '恋情詩歌', 'medium_picture': 'https://cdn.myanimelist.net/images/anime/1164/137261.jpg'},
"medium_picture": "https://cdn.myanimelist.net/images/anime/1164/137261.jpg"
},
{
"id": 54667,
"title": "Mukashibanashi no Oheya: Tsutaetai Nihon Mukashibanashi",
"alternative_titles": {'synonyms': [], 'en': '', 'ja': 'むかしばなしのおへや\u3000〜伝えたい日本昔話〜', 'medium_picture': 'https://cdn.myanimelist.net/images/anime/1384/133998.jpg'},
"medium_picture": "https://cdn.myanimelist.net/images/anime/1384/133998.jpg"
},
{
"id": 55933,
"title": "Youtiful",
"alternative_titles": {'synonyms': [], 'en': '', 'ja': 'Youtiful', 'medium_picture': 'https://cdn.myanimelist.net/images/anime/1245/137072.jpg'},
"medium_picture": "https://cdn.myanimelist.net/images/anime/1245/137072.jpg"
},
{
"id": 55891,
"title": "Uchuu Sanpo",
"alternative_titles": {'synonyms': ['Space Walk'], 'en': 'Cosmic Rendezvous', 'ja': '宇宙散歩', 'medium_picture': 'https://cdn.myanimelist.net/images/anime/1276/137003.jpg'},
"medium_picture": "https://cdn.myanimelist.net/images/anime/1276/137003.jpg"
},
{
"id": 56041,
"title": "Long Shidai",
"alternative_titles": {'synonyms': ['X Epoch of Dragon'], 'en': 'Epoch of Dragon', 'ja': '龙时代', 'medium_picture': 'https://cdn.myanimelist.net/images/anime/1431/137280.jpg'},
"medium_picture": "https://cdn.myanimelist.net/images/anime/1431/137280.jpg"
},
{
"id": 56032,
"title": "Shinbigan",
"alternative_titles": {'synonyms': [], 'en': 'Aesthetic Sense', 'ja': '審美眼', 'medium_picture': 'https://cdn.myanimelist.net/images/anime/1765/137253.jpg'},
"medium_picture": "https://cdn.myanimelist.net/images/anime/1765/137253.jpg"
},
{
"id": 56040,
"title": "Shi Wangzhe A? 2nd Season",
"alternative_titles": {'synonyms': [], 'en': '', 'ja': '是王者啊? 第二季', 'medium_picture': 'https://cdn.myanimelist.net/images/anime/1146/137284.jpg'},
"medium_picture": "https://cdn.myanimelist.net/images/anime/1146/137284.jpg"
},
{
"id": 55929,
"title": "S-Class (SKZOO ver.)",
"alternative_titles": {'synonyms': [], 'en': '', 'ja': '특S-Class (SKZOO ver.)', 'medium_picture': 'https://cdn.myanimelist.net/images/anime/1423/137092.jpg'},
"medium_picture": "https://cdn.myanimelist.net/images/anime/1423/137092.jpg"
},
{
"id": 55948,
"title": "Sylvanian Families: Freya no Go for Dream!",
"alternative_titles": {'synonyms': [], 'en': '', 'ja': 'シルバニアファミリー フレアのゴー・フォー・ドリーム！', 'medium_picture': 'https://cdn.myanimelist.net/images/anime/1455/137080.jpg'},
"medium_picture": "https://cdn.myanimelist.net/images/anime/1455/137080.jpg"
},
{
"id": 55939,
"title": "Synduality: Kagaku Kouza",
"alternative_titles": {'synonyms': [], 'en': '', 'ja': 'シンデュアリティ科学講座', 'medium_picture': 'https://cdn.myanimelist.net/images/anime/1543/137089.jpg'},
"medium_picture": "https://cdn.myanimelist.net/images/anime/1543/137089.jpg"
},
{
"id": 56006,
"title": "Twilight Little Star",
"alternative_titles": {'synonyms': [], 'en': '', 'ja': 'twilight little star', 'medium_picture': 'https://cdn.myanimelist.net/images/anime/1141/137186.jpg'},
"medium_picture": "https://cdn.myanimelist.net/images/anime/1141/137186.jpg"
},
{
"id": 55694,
"title": "Gaishi Dizun",
"alternative_titles": {'synonyms': [], 'en': '', 'ja': '盖世帝尊', 'medium_picture': 'https://cdn.myanimelist.net/images/anime/1885/136527.jpg'},
"medium_picture": "https://cdn.myanimelist.net/images/anime/1885/136527.jpg"
},
{
"id": 54871,
"title": "Shin Nippon History",
"alternative_titles": {'synonyms': ['Shin Nippon History: Minna ga Shiranai, Atarashii Nihon no Rekishi.'], 'en': '', 'ja': '新ニッポンヒストリー', 'medium_picture': 'https://cdn.myanimelist.net/images/anime/1433/134811.jpg'},
"medium_picture": "https://cdn.myanimelist.net/images/anime/1433/134811.jpg"
},
{
"id": 55920,
"title": "Ahiru-kun no Chiisana Bouken",
"alternative_titles": {'synonyms': [], 'en': "Duck's Little Adventure", 'ja': 'アヒルくんの小さな冒険', 'medium_picture': 'https://cdn.myanimelist.net/images/anime/1110/137061.jpg'},
"medium_picture": "https://cdn.myanimelist.net/images/anime/1110/137061.jpg"
},
{
"id": 53830,
"title": "Poporisu & Friends",
"alternative_titles": {'synonyms': [], 'en': '', 'ja': 'ぽぽりす＆フレンズ', 'medium_picture': 'https://cdn.myanimelist.net/images/anime/1419/131792.jpg'},
"medium_picture": "https://cdn.myanimelist.net/images/anime/1419/131792.jpg"
},
{
"id": 55746,
"title": "Feng Huo Zhan Ji",
"alternative_titles": {'synonyms': [], 'en': '', 'ja': '风火战纪', 'medium_picture': 'https://cdn.myanimelist.net/images/anime/1460/136627.jpg'},
"medium_picture": "https://cdn.myanimelist.net/images/anime/1460/136627.jpg"
},
{
"id": 55957,
"title": "Higeki no Genkyou to Naru Saikyou Gedou Last Boss Joou wa Tami no Tame ni Tsukushimasu. Mini",
"alternative_titles": {'synonyms': [], 'en': 'The Most Heretical Last Boss Queen: From Villainess to Savior Mini Anime', 'ja': '悲劇の元凶となる最強外道ラスボス女王は民の為に尽くします。ミニ', 'medium_picture': 'https://cdn.myanimelist.net/images/anime/1620/137131.jpg'},
"medium_picture": "https://cdn.myanimelist.net/images/anime/1620/137131.jpg"
},
{
"id": 54945,
"title": "Chang An San Wan Li",
"alternative_titles": {'synonyms': ['Chang An'], 'en': "30,000 Miles From Chang'an", 'ja': '长安三万里', 'medium_picture': 'https://cdn.myanimelist.net/images/anime/1580/135219.jpg'},
"medium_picture": "https://cdn.myanimelist.net/images/anime/1580/135219.jpg"
},
{
"id": 56064,
"title": "Kimi ni Aeta!",
"alternative_titles": {'synonyms': ['Pokemon WCS2023'], 'en': '', 'ja': 'キミに会えた！', 'medium_picture': 'https://cdn.myanimelist.net/images/anime/1706/137331.jpg'},
"medium_picture": "https://cdn.myanimelist.net/images/anime/1706/137331.jpg"
},
{
"id": 55732,
"title": "Bu Xing Si: Yuan Qi",
"alternative_titles": {'synonyms': [], 'en': 'Blader Soul', 'ja': '捕星司·源起', 'medium_picture': 'https://cdn.myanimelist.net/images/anime/1383/136861.jpg'},
"medium_picture": "https://cdn.myanimelist.net/images/anime/1383/136861.jpg"
},
{
"id": 48442,
"title": "Shikaru Neko",
"alternative_titles": {'synonyms': [], 'en': '', 'ja': 'しかるねこ', 'medium_picture': 'https://cdn.myanimelist.net/images/anime/1008/113384.jpg'},
"medium_picture": "https://cdn.myanimelist.net/images/anime/1008/113384.jpg"
},
{
"id": 54495,
"title": "Kyoukai Senki: Kyokkou no Souki",
"alternative_titles": {'synonyms': [], 'en': '', 'ja': '境界戦機 極鋼ノ装鬼', 'medium_picture': 'https://cdn.myanimelist.net/images/anime/1679/135836.jpg'},
"medium_picture": "https://cdn.myanimelist.net/images/anime/1679/135836.jpg"
},
{
"id": 51585,
"title": "City Hunter Movie: Tenshi no Namida",
"alternative_titles": {'synonyms': [], 'en': 'City Hunter The Movie: Angel Dust', 'ja': '劇場版シティーハンター 天使の涙 (エンジェルダスト)', 'medium_picture': 'https://cdn.myanimelist.net/images/anime/1046/136433.jpg'},
"medium_picture": "https://cdn.myanimelist.net/images/anime/1046/136433.jpg"
},
{
"id": 49793,
"title": "Azur Lane: Queen's Orders",
"alternative_titles": {'synonyms': [], 'en': '', 'ja': "アズールレーン Queen's Orders", 'medium_picture': 'https://cdn.myanimelist.net/images/anime/1602/133747.jpg'},
"medium_picture": "https://cdn.myanimelist.net/images/anime/1602/133747.jpg"
},
{
"id": 53882,
"title": "Sand Land",
"alternative_titles": {'synonyms': [], 'en': 'Sand Land', 'ja': 'SAND LAND', 'medium_picture': 'https://cdn.myanimelist.net/images/anime/1834/136339.jpg'},
"medium_picture": "https://cdn.myanimelist.net/images/anime/1834/136339.jpg"
},
{
"id": 53720,
"title": "Hi no Tori: Eden no Sora",
"alternative_titles": {'synonyms': [], 'en': 'PHOENIX: EDEN17', 'ja': '火の鳥 エデンの宙', 'medium_picture': 'https://cdn.myanimelist.net/images/anime/1599/134699.jpg'},
"medium_picture": "https://cdn.myanimelist.net/images/anime/1599/134699.jpg"
},
{
"id": 54650,
"title": "Precure All Stars Movie F",
"alternative_titles": {'synonyms': ['Pretty Cure All Stars Movie F'], 'en': '', 'ja': '映画プリキュアオールスターズF', 'medium_picture': 'https://cdn.myanimelist.net/images/anime/1959/137024.jpg'},
"medium_picture": "https://cdn.myanimelist.net/images/anime/1959/137024.jpg"
},
{
"id": 53627,
"title": "Gamera: Rebirth",
"alternative_titles": {'synonyms': [], 'en': '', 'ja': 'GAMERA -Rebirth-', 'medium_picture': 'https://cdn.myanimelist.net/images/anime/1024/134654.jpg'},
"medium_picture": "https://cdn.myanimelist.net/images/anime/1024/134654.jpg"
},
{
"id": 30151,
"title": "Kamiusagi Rope: Warau Asa ni wa Fukuraitaru tte Maji ssuka!?",
"alternative_titles": {'synonyms': ['Kamiusagi Rope 4'], 'en': '', 'ja': '紙兎ロペ 〜笑う朝には福来たるってマジっすか!?', 'medium_picture': 'https://cdn.myanimelist.net/images/anime/6/72182.jpg'},
"medium_picture": "https://cdn.myanimelist.net/images/anime/6/72182.jpg"
},
{
"id": 55578,
"title": "Si Ge Yongzhe",
"alternative_titles": {'synonyms': [], 'en': '4 Cut Hero', 'ja': '四格勇者', 'medium_picture': 'https://cdn.myanimelist.net/images/anime/1319/136330.jpg'},
"medium_picture": "https://cdn.myanimelist.net/images/anime/1319/136330.jpg"
},
{
"id": 49120,
"title": "Osomatsu-san: Tamashii no Takoyaki Party to Densetsu no Otomarikai",
"alternative_titles": {'synonyms': ['Mr. Osomatsu'], 'en': '', 'ja': 'おそ松さん~魂のたこ焼きパーティーと伝説のお泊り会~', 'medium_picture': 'https://cdn.myanimelist.net/images/anime/1026/136351.jpg'},
"medium_picture": "https://cdn.myanimelist.net/images/anime/1026/136351.jpg"
},
{
"id": 54122,
"title": "Ooyukiumi no Kaina: Hoshi no Kenja",
"alternative_titles": {'synonyms': [], 'en': 'Kaina of the Great Snow Sea: Star Sage', 'ja': '大雪海のカイナ ほしのけんじゃ', 'medium_picture': 'https://cdn.myanimelist.net/images/anime/1182/136415.jpg'},
"medium_picture": "https://cdn.myanimelist.net/images/anime/1182/136415.jpg"
},
{
"id": 53911,
"title": "Nanatsu no Taizai: Ensa no Edinburgh Part 2",
"alternative_titles": {'synonyms': [], 'en': 'The Seven Deadly Sins: Grudge of Edinburgh Part 2', 'ja': '七つの大罪 怨嗟のエジンバラ 後編', 'medium_picture': 'https://cdn.myanimelist.net/images/anime/1597/137276.jpg'},
"medium_picture": "https://cdn.myanimelist.net/images/anime/1597/137276.jpg"
},
{
"id": 52701,
"title": "Dungeon Meshi",
"alternative_titles": {'synonyms': ['Dungeon Food'], 'en': 'Delicious in Dungeon', 'ja': 'ダンジョン飯', 'medium_picture': 'https://cdn.myanimelist.net/images/anime/1830/136116.jpg'},
"medium_picture": "https://cdn.myanimelist.net/images/anime/1830/136116.jpg"
},
{
"id": 51318,
"title": "Hanma Baki: Son of Ogre 2nd Season",
"alternative_titles": {'synonyms': ['The Boy Fascinating the Fighting God'], 'en': 'Baki Hanma 2nd Season', 'ja': '範馬刃牙 SON OF OGRE', 'medium_picture': 'https://cdn.myanimelist.net/images/anime/1800/135847.jpg'},
"medium_picture": "https://cdn.myanimelist.net/images/anime/1800/135847.jpg"
},
{
"id": 49303,
"title": "Alice to Therese no Maboroshi Koujou",
"alternative_titles": {'synonyms': ["Alice and Therese's Illusion Factory", 'The Illusion Factory of Alice and Therese'], 'en': 'Maboroshi', 'ja': 'アリスとテレスのまぼろし工場', 'medium_picture': 'https://cdn.myanimelist.net/images/anime/1429/137275.jpg'},
"medium_picture": "https://cdn.myanimelist.net/images/anime/1429/137275.jpg"
},
{
"id": 47160,
"title": "Goblin Slayer II",
"alternative_titles": {'synonyms': ['Goblin Slayer 2nd Season'], 'en': '', 'ja': 'ゴブリンスレイヤー II', 'medium_picture': 'https://cdn.myanimelist.net/images/anime/1569/134760.jpg'},
"medium_picture": "https://cdn.myanimelist.net/images/anime/1569/134760.jpg"
},
{
"id": 51369,
"title": "Kengan Ashura Season 2",
"alternative_titles": {'synonyms': ['Kengan Ashura 2nd Season'], 'en': '', 'ja': 'ケンガンアシュラ', 'medium_picture': 'https://cdn.myanimelist.net/images/anime/1513/134619.jpg'},
"medium_picture": "https://cdn.myanimelist.net/images/anime/1513/134619.jpg"
},
{
"id": 54688,
"title": "Naruto (Shinsaku Anime)",
"alternative_titles": {'synonyms': [], 'en': '', 'ja': 'ナルト新作アニメ', 'medium_picture': 'https://cdn.myanimelist.net/images/anime/1378/137310.jpg'},
"medium_picture": "https://cdn.myanimelist.net/images/anime/1378/137310.jpg"
},
{
"id": 50407,
"title": "Wu Shan Wu Xing (2020): Xichuan Huan Zi Lin",
"alternative_titles": {'synonyms': ['Wu Shan Wu Xing 2nd Season'], 'en': 'Fog Hill of Five Elements', 'ja': '雾山五行·犀川幻紫林', 'medium_picture': 'https://cdn.myanimelist.net/images/anime/1433/119529.jpg'},
"medium_picture": "https://cdn.myanimelist.net/images/anime/1433/119529.jpg"
},
{
"id": 54141,
"title": "Bastard!! Ankoku no Hakaishin Season 2 (ONA)",
"alternative_titles": {'synonyms': [], 'en': 'Bastard‼ Heavy Metal, Dark Fantasy Season 2', 'ja': 'BASTARD!! -暗黒の破壊神- 2', 'medium_picture': 'https://cdn.myanimelist.net/images/anime/1268/137255.jpg'},
"medium_picture": "https://cdn.myanimelist.net/images/anime/1268/137255.jpg"
},
{
"id": 51995,
"title": "Hibike! Euphonium: Ensemble Contest-hen",
"alternative_titles": {'synonyms': ['Sound! Euphonium: Ensemble Contest Arc'], 'en': '', 'ja': '『響け！ユーフォニアム』アンサンブルコンテスト編', 'medium_picture': 'https://cdn.myanimelist.net/images/anime/1952/135162.jpg'},
"medium_picture": "https://cdn.myanimelist.net/images/anime/1952/135162.jpg"
},
{
"id": 53810,
"title": "Crayon Shin-chan Movie 31: Chounouryoku Daikessen - Tobe Tobe Temakizushi",
"alternative_titles": {'synonyms': ['Shin Jigen! Crayon Shin-chan the Movie: Chounouryoku Daikessen - Tobe Tobe Temakizushi'], 'en': '', 'ja': 'しん次元! クレヨンしんちゃんTHE MOVIE 超能力大決戦 ~とべとべ手巻き寿司~', 'medium_picture': 'https://cdn.myanimelist.net/images/anime/1431/136322.jpg'},
"medium_picture": "https://cdn.myanimelist.net/images/anime/1431/136322.jpg"
},
{
"id": 54630,
"title": "Bosanimal",
"alternative_titles": {'synonyms': [], 'en': '', 'ja': 'ぼさにまる', 'medium_picture': 'https://cdn.myanimelist.net/images/anime/1360/133846.jpg'},
"medium_picture": "https://cdn.myanimelist.net/images/anime/1360/133846.jpg"
},
{
"id": 29375,
"title": "Robot Pulta",
"alternative_titles": {'synonyms': ['Robot Apartments', 'Robot Paruta'], 'en': '', 'ja': 'ロボット・パルタ', 'medium_picture': 'https://cdn.myanimelist.net/images/anime/9/70637.jpg'},
"medium_picture": "https://cdn.myanimelist.net/images/anime/9/70637.jpg"
},
{
"id": 30119,
"title": "Yowamushi Monsters",
"alternative_titles": {'synonyms': ['Yowamon'], 'en': '', 'ja': 'よわむしモンスターズ', 'medium_picture': 'https://cdn.myanimelist.net/images/anime/11/72127.jpg'},
"medium_picture": "https://cdn.myanimelist.net/images/anime/11/72127.jpg"
},
{
"id": 22669,
"title": "Gohan Kaijuu Pap",
"alternative_titles": {'synonyms': ['Rice Monster Pap'], 'en': '', 'ja': 'ごはんかいじゅうパップ', 'medium_picture': 'https://cdn.myanimelist.net/images/anime/13/59289.jpg'},
"medium_picture": "https://cdn.myanimelist.net/images/anime/13/59289.jpg"
},
{
"id": 55684,
"title": "Yong Sheng: Shi Nian Zhi Yue",
"alternative_titles": {'synonyms': ['Yong Sheng 2nd Season'], 'en': 'Immortality 2nd Season', 'ja': '永生 之十年之约', 'medium_picture': 'https://cdn.myanimelist.net/images/anime/1872/136499.jpg'},
"medium_picture": "https://cdn.myanimelist.net/images/anime/1872/136499.jpg"
},
{
"id": 55733,
"title": "Di Yi Xulie",
"alternative_titles": {'synonyms': [], 'en': 'The First Order', 'ja': '第一序列', 'medium_picture': 'https://cdn.myanimelist.net/images/anime/1130/137242.jpg'},
"medium_picture": "https://cdn.myanimelist.net/images/anime/1130/137242.jpg"
},
{
"id": 35696,
"title": "Konigiri-kun",
"alternative_titles": {'synonyms': [], 'en': '', 'ja': 'こにぎりくん', 'medium_picture': 'https://cdn.myanimelist.net/images/anime/8/86112.jpg'},
"medium_picture": "https://cdn.myanimelist.net/images/anime/8/86112.jpg"
},
{
"id": 35698,
"title": "Oidon to",
"alternative_titles": {'synonyms': [], 'en': '', 'ja': 'おいどんと', 'medium_picture': 'https://cdn.myanimelist.net/images/anime/13/86114.jpg'},
"medium_picture": "https://cdn.myanimelist.net/images/anime/13/86114.jpg"
},
{
"id": 35372,
"title": "Otoppe",
"alternative_titles": {'synonyms': [], 'en': '', 'ja': 'オトッペ', 'medium_picture': 'https://cdn.myanimelist.net/images/anime/4/85180.jpg'},
"medium_picture": "https://cdn.myanimelist.net/images/anime/4/85180.jpg"
},
{
"id": 54762,
"title": "Duel Masters Win: Duel Wars-hen",
"alternative_titles": {'synonyms': [], 'en': '', 'ja': 'デュエル・マスターズ WIN 決闘学園（デュエル・ウォーズ）編', 'medium_picture': 'https://cdn.myanimelist.net/images/anime/1618/134534.jpg'},
"medium_picture": "https://cdn.myanimelist.net/images/anime/1618/134534.jpg"
},
{
"id": 29421,
"title": "Liv & Bell",
"alternative_titles": {'synonyms': ['Liv and Bell'], 'en': 'Liv & Bell', 'ja': 'リヴ＆ベル', 'medium_picture': 'https://cdn.myanimelist.net/images/anime/6/70717.jpg'},
"medium_picture": "https://cdn.myanimelist.net/images/anime/6/70717.jpg"
},
{
"id": 55790,
"title": "Zhen Hun Jie 3rd Season",
"alternative_titles": {'synonyms': ['Requiem Street 3rd Season'], 'en': 'Rakshasa Street 3rd Season', 'ja': '镇魂街 第三季', 'medium_picture': 'https://cdn.myanimelist.net/images/anime/1080/136724.jpg'},
"medium_picture": "https://cdn.myanimelist.net/images/anime/1080/136724.jpg"
},
{
"id": 38776,
"title": "Manul no Yuube",
"alternative_titles": {'synonyms': [], 'en': '', 'ja': 'マヌ～ルのゆうべ', 'medium_picture': 'https://cdn.myanimelist.net/images/anime/1980/96936.jpg'},
"medium_picture": "https://cdn.myanimelist.net/images/anime/1980/96936.jpg"
},
{
"id": 50522,
"title": "Teikou Penguin",
"alternative_titles": {'synonyms': [], 'en': '', 'ja': 'テイコウペンギン', 'medium_picture': 'https://cdn.myanimelist.net/images/anime/1018/119890.jpg'},
"medium_picture": "https://cdn.myanimelist.net/images/anime/1018/119890.jpg"
},
{
"id": 42870,
"title": "Uchuu Nanchara Kotetsu-kun",
"alternative_titles": {'synonyms': [], 'en': 'Space Academy', 'ja': '宇宙なんちゃらこてつくん', 'medium_picture': 'https://cdn.myanimelist.net/images/anime/1226/112286.jpg'},
"medium_picture": "https://cdn.myanimelist.net/images/anime/1226/112286.jpg"
},
{
"id": 10506,
"title": "Shiawase Haitatsu Taneko",
"alternative_titles": {'synonyms': [], 'en': '', 'ja': 'しあわせ配達おみくじタネコ', 'medium_picture': 'https://cdn.myanimelist.net/images/anime/2/28900.jpg'},
"medium_picture": "https://cdn.myanimelist.net/images/anime/2/28900.jpg"
},
{
"id": 55762,
"title": "Ququ Bucai, Zaixia Yeguai 2nd Season",
"alternative_titles": {'synonyms': ['怎么办! 我穿越成了最弱小野怪', 'Zenmeban! Wo Chuanyue Cheng Le Zui Ruoxiao Ye Guai', 'What Do I Do?! I Have Transmigrated Into the Weakest Little Monster'], 'en': 'Monster But Wild 2nd Season', 'ja': '区区不才，在下野怪 第二季', 'medium_picture': 'https://cdn.myanimelist.net/images/anime/1530/136847.jpg'},
"medium_picture": "https://cdn.myanimelist.net/images/anime/1530/136847.jpg"
},
{
"id": 53079,
"title": "Youjo Shachou R",
"alternative_titles": {'synonyms': ['Youjo Shachou 2nd Season', 'Cute Executive Officer 2nd Season'], 'en': 'Cute Executive Officer R', 'ja': '幼女社長 R', 'medium_picture': 'https://cdn.myanimelist.net/images/anime/1052/136246.jpg'},
"medium_picture": "https://cdn.myanimelist.net/images/anime/1052/136246.jpg"
},
{
"id": 55692,
"title": "Feng Ling Yu Xiu 2nd Season",
"alternative_titles": {'synonyms': [], 'en': '', 'ja': '风灵玉秀 第二章', 'medium_picture': 'https://cdn.myanimelist.net/images/anime/1634/136523.jpg'},
"medium_picture": "https://cdn.myanimelist.net/images/anime/1634/136523.jpg"
},
{
"id": 29427,
"title": "Mori no Ratio",
"alternative_titles": {'synonyms': ['Mori no Reshio'], 'en': 'Ratio of Forest', 'ja': '森のレシオ', 'medium_picture': 'https://cdn.myanimelist.net/images/anime/8/70899.jpg'},
"medium_picture": "https://cdn.myanimelist.net/images/anime/8/70899.jpg"
},
{
"id": 18941,
"title": "Shimajirou no Wow!",
"alternative_titles": {'synonyms': [], 'en': '', 'ja': 'しまじろうのわお!', 'medium_picture': 'https://cdn.myanimelist.net/images/anime/9/50737.jpg'},
"medium_picture": "https://cdn.myanimelist.net/images/anime/9/50737.jpg"
},
{
"id": 54847,
"title": "Ikimono-san",
"alternative_titles": {'synonyms': [], 'en': '', 'ja': 'いきものさん', 'medium_picture': 'https://cdn.myanimelist.net/images/anime/1466/136270.jpg'},
"medium_picture": "https://cdn.myanimelist.net/images/anime/1466/136270.jpg"
},
{
"id": 35695,
"title": "Keito no Yousei: Knit to Wool",
"alternative_titles": {'synonyms': [], 'en': '', 'ja': 'けいとのようせいニットとウール', 'medium_picture': 'https://cdn.myanimelist.net/images/anime/2/86111.jpg'},
"medium_picture": "https://cdn.myanimelist.net/images/anime/2/86111.jpg"
},
]





# Function to read anime scores from the CSV file
def get_anime_scores():
    anime_scores = []
    with open(csv_file, "r") as csvfile:
        csv_reader = csv.reader(csvfile)
        for row in csv_reader:
            if row[0] == "---":  # Indicator for gap, skip this row
                continue
            anime_id = int(row[0])
            score = float(row[1])
            timestamp = datetime.strptime(row[2], "%Y-%m-%d %H:%M:%S")  # Corrected timestamp format
            anime_scores.append((anime_id, score, timestamp))
    return anime_scores

# Function to plot the line chart for anime scores
def plot_line_chart(anime_id):
    anime_scores = get_anime_scores()
    filtered_scores = [score for score in anime_scores if score[0] == anime_id]
    timestamps = [score[2] for score in filtered_scores]
    scores = [score[1] for score in filtered_scores]

    fig = make_subplots(rows=1, cols=1)
    fig.add_trace(go.Scatter(x=timestamps, y=scores, mode='lines', name='Anime Score'))

    fig.update_layout(title_text=f"Line Chart for Anime ID: {anime_id}",
                      xaxis_title="Timestamp",
                      yaxis_title="Score")

    return fig

def get_anime_data(anime_id):
    client_id = "ed4a7c958707ea1a3ea5e22958c69ebd"
    headers = {
        "X-MAL-CLIENT-ID": client_id,
          # Replace YOUR_TOKEN with your access token
    }

    url = f"https://api.myanimelist.net/v2/anime/{anime_id}?fields=id,title,mean"
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        anime_title = data.get("title", "")
        mean_score = data.get("mean", None)
        return anime_title, mean_score
    else:
        return None, None
    
def get_mean_score(anime_id):
    _, mean_score = get_anime_data(anime_id)
    return mean_score

def p_multiplicator_generator(anime_id):
    # Function to fetch the PL Multiplier for the given anime_id from the database
    conn = sqlite3.connect('anime_data.db')
    cursor = conn.cursor()

    # Check if the anime_id exists in any of the popularity category tables
    cursor.execute('''
        SELECT * FROM high_popularity_anime WHERE anime_id = ?
    ''', (anime_id,))
    row = cursor.fetchone()
    if row:
        pl_multiplier = row[3]  # Index 3 contains the PL Multiplier
        conn.close()
        return pl_multiplier

    cursor.execute('''
        SELECT * FROM moderate_popularity_anime WHERE anime_id = ?
    ''', (anime_id,))
    row = cursor.fetchone()
    if row:
        pl_multiplier = row[3]
        conn.close()
        return pl_multiplier

    cursor.execute('''
        SELECT * FROM low_popularity_anime WHERE anime_id = ?
    ''', (anime_id,))
    row = cursor.fetchone()
    if row:
        pl_multiplier = row[3]
        conn.close()
        return pl_multiplier

    conn.close()

    # If the anime_id does not exist in any of the tables, return None
    return None

def write_to_user_investment_csv(file_path, user_data_list):
    # Function to write user investment data to CSV file
    with open(file_path, "a", newline="", encoding="utf-8") as csvfile:
        fieldnames = [
            "Investment Type", "Anime ID", "Anime Title", "Name",
            "UPDATED Score", "Start Date", "End Date",
            "Target", "Limiter", "Investing Amount", "PL Multiplier",
            "Investment Duration", "new_amount", "profit", "loss"  # Add the new fields for new_amount, profit, and loss
        ]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        # Check if the CSV file is empty
        if csvfile.tell() == 0:
            writer.writeheader()
        # Write the new user data with Investment Duration, new_amount, profit, and loss values
        for user_data in user_data_list:
            user_data["Investment Duration"] = calculate_investment_duration(user_data)
            writer.writerow(user_data)


def calculate_investment_duration(user_data):
    # Function to calculate the investment duration based on start and end dates
    start_date = datetime.strptime(user_data["Start Date"], "%d-%m-%Y")
    end_date = datetime.strptime(user_data["End Date"], "%d-%m-%Y")
    duration = end_date - start_date

    # Return the duration in days
    return duration.days

scheduler = BackgroundScheduler()

def fetch_user_investments():
    # Function to fetch user investments from the CSV
    user_investments = []
    with open('user_investment.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            user_investments.append(row)
    return user_investments

def start_profit_function(user_data):
    # Function to handle profit calculation
    # Get the necessary data from user_data
    investing_amount = float(user_data["Investing Amount"])
    pl_multiplier = float(user_data["PL Multiplier"])
    updated_score = float(user_data["UPDATED Score"])
    target = float(user_data["Target"])  # Get the target value from user_data
    investment_type = user_data["Investment Type"]  # Get the investment type

    if investment_type == "BUY(HIGH)":
        # Calculate the newamount using the formula for BUY(HIGH)
        newamount = investing_amount + (pl_multiplier * 100) + (target - updated_score) * 10
    elif investment_type == "BUY(LOW)":
        # Calculate the newamount using the formula for BUY(LOW)
        newamount = investing_amount + (pl_multiplier * 100) + (updated_score - target) * 10
    else:
        # Invalid investment type, return 0
        newamount = 0

    # Update the global balance with the new amount (if newamount is positive)
    global balance
    if newamount > 0:
        balance += newamount

    return max(0, newamount)


def start_loss_function(user_data):
    # Function to handle loss calculation
    # Get today's date
    today_date = datetime.now().strftime("%d-%m-%Y")

    # Check if today's date is equal to the end date
    end_date = datetime.strptime(user_data["End Date"], "%d-%m-%Y")

    if today_date == end_date.strftime("%d-%m-%Y"):
        # Logic for handling the loss when today's date is equal to the end date

        # Get the necessary data from user_data
        investing_amount = float(user_data["Investing Amount"])
        pl_multiplier = float(user_data["PL Multiplier"])
        updated_score = float(user_data["UPDATED Score"])
        limiter = user_data.get("Limiter", None)
        investment_type = user_data["Investment Type"]  # Get the investment type

        if investment_type == "BUY(HIGH)":
            # Calculate loss_gen based on limiter or lowest_score for BUY(HIGH)
            if limiter is not None:
                # Calculate loss_gen using the limiter value
                loss_gen = updated_score - float(limiter)
            else:
                # Calculate lowest_score from anime_scores.csv for BUY(HIGH)
                anime_id = int(user_data["Anime ID"])
                lowest_score = fetch_least_score(anime_id)

                # Ensure that lowest_score is less than updated_score
                if lowest_score >= updated_score:
                    lowest_score = updated_score

                # Calculate loss_gen using the lowest_score value
                loss_gen = updated_score - lowest_score

        elif investment_type == "BUY(LOW)":
            # Calculate loss_gen based on limiter or highest_score for BUY(LOW)
            if limiter is not None:
                # Calculate loss_gen using the limiter value
                loss_gen = float(limiter) - updated_score
            else:
                # Calculate highest_score from anime_scores.csv for BUY(LOW)
                anime_id = int(user_data["Anime ID"])
                highest_score = fetch_highest_score(anime_id)

                # Ensure that highest_score is more than updated_score
                if highest_score <= updated_score:
                    highest_score = updated_score

                # Calculate loss_gen using the highest_score value
                loss_gen = highest_score - updated_score
        else:
            # Invalid investment type, return 0
            return 0

        # Calculate newamount using the loss_gen
        newamount = investing_amount - (pl_multiplier * 100) - abs(loss_gen) * 10
        newamount2 = abs(newamount)

        # Update the global balance with the new amount (if newamount is positive)
        global balance
        balance -= newamount2

        return max(0, newamount)

    else:
        print("No changes in the investment.")

def fetch_highest_score(anime_id):
    # Function to fetch the highest score for an anime_id from anime_scores.csv
    highest_score = None

    # Read the data from the anime_scores.csv file
    with open('anime_scores.csv', newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            # Check if the first column (anime_id) matches the target anime_id
            if row[0] == str(anime_id):
                # Parse the score from the second column
                score = float(row[1])

                # Update the highest_score if it's None or higher than the current score
                if highest_score is None or score > highest_score:
                    highest_score = score

    return highest_score if highest_score is not None else 9.0  # Assuming the highest possible score is 5.0

def fetch_least_score(anime_id):
    # Function to fetch the least score for an anime_id from anime_scores.csv
    lowest_score = None

    # Read the data from the anime_scores.csv file
    with open('anime_scores.csv', newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            # Check if the first column (anime_id) matches the target anime_id
            if row[0] == str(anime_id):
                # Parse the score from the second column
                score = float(row[1])

                # Update the lowest_score if it's None or lower than the current score
                if lowest_score is None or score < lowest_score:
                    lowest_score = score

    return lowest_score if lowest_score is not None else 0.0

def check_order_status(user_data):
    newamount = None
     
    global balance  # Access the global balance variable

    # Get today's date
    today_date = datetime.now().strftime("%d-%m-%Y")

    # Check if today's date is between the start date and end date (inclusive)
    start_date = datetime.strptime(user_data["Start Date"], "%d-%m-%Y")
    end_date = datetime.strptime(user_data["End Date"], "%d-%m-%Y")

    if start_date <= datetime.now() <= end_date:
        # Fetch the mean score using the anime_id
        anime_id = int(user_data["Anime ID"])
        mean_score = fetch_mean_score(anime_id)
        if mean_score is not None:
            # Perform other actions or calculations here if needed
            print("Order is active and mean score is:", mean_score)

            # Check the type of order (BUY_HIGH or BUY_LOW) and execute the appropriate function
            order_type = user_data["Investment Type"]
            target = float(user_data["Target"])
            if order_type == "BUY(HIGH)":
                if mean_score >= target:
                    newamount = start_profit_function(user_data)
                    # Remove the user investment data from the CSV if profits are achieved
                    if newamount is not None and newamount > 0:
                        remove_user_investment(user_data)
                else:
                    newamount = start_loss_function(user_data)
            elif order_type == "BUY(LOW)":
                if mean_score <= target:
                    newamount = start_profit_function(user_data)
                    # Remove the user investment data from the CSV if profits are achieved
                    if newamount is not None and newamount > 0:
                        remove_user_investment(user_data)
                else:
                    newamount = start_loss_function(user_data)
            else:
                print("Invalid order type:", order_type)

        else:
            print("Anime data not found for anime_id:", anime_id)

    else:
        print("Your order has expired.")
        remove_user_investment(user_data)
        
    # Update the user_data with the new_amount, profit, and loss values (even if newamount is None)
    user_data["new_amount"] = newamount
    if newamount is not None:
        if newamount > float(user_data["Investing Amount"]):
            user_data["profit"] = f"PROFIT OF ({newamount - float(user_data['Investing Amount']):.2f})"
            user_data["loss"] = ""
        else:
            user_data["loss"] = f"LOSS OF ({float(user_data['Investing Amount']) - abs(newamount):.2f})"
            user_data["profit"] = ""
    else:
        # If newamount is None, set profit and loss to empty strings
        user_data["profit"] = ""
        user_data["loss"] = ""


def remove_user_investment(user_data):
    # Fetch all user investments from the CSV
    user_investments = fetch_user_investments()

    # Check if the user_investments list is not empty
    if not user_investments:
        print("No user investments found.")
        return

    # Fetch the index of the user_data in the list of investments
    index_to_remove = None
    for i, investment_data in enumerate(user_investments):
        if (
            investment_data["Investment Type"] == user_data["Investment Type"]
            and investment_data["Anime ID"] == user_data["Anime ID"]
            and investment_data["Anime Title"] == user_data["Anime Title"]
            and investment_data["Name"] == user_data["Name"]
            and investment_data["Start Date"] == user_data["Start Date"]
            and investment_data["End Date"] == user_data["End Date"]
            and investment_data["Investing Amount"] == user_data["Investing Amount"]
        ):
            index_to_remove = i
            break

    if index_to_remove is not None:
        # Remove the user investment data from the list
        removed_investment = user_investments.pop(index_to_remove)

        # Write the updated user investment data back to the CSV file
        with open('user_investment.csv', "w", newline="", encoding="utf-8") as csvfile:
            fieldnames = removed_investment.keys()
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(user_investments)
        print("User investment removed successfully.")
    else:
        print("User investment not found.")


def fetch_mean_score(anime_id):
    client_id = "ed4a7c958707ea1a3ea5e22958c69ebd"
    headers = {"X-MAL-CLIENT-ID": client_id}
    url = f"https://api.myanimelist.net/v2/anime/{anime_id}?fields=mean"
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        mean_score = data.get("mean", None)
        return mean_score
    else:
        return None
    
# Function to update user investments and check order status
def update_user_investments():
    global balance

    # Create a list to store changes in investments
    investment_changes = []

    user_investments = fetch_user_investments()
    for user_data in user_investments:
        if not user_data["Investing Amount"]:
            # Skip user investment data with an empty "Investing Amount"
            continue

        # Check if the order has expired and remove it from the user investment table
        start_date = datetime.strptime(user_data["Start Date"], "%d-%m-%Y")
        end_date = datetime.strptime(user_data["End Date"], "%d-%m-%Y")
        if datetime.now() < start_date or datetime.now() > end_date:
            remove_user_investment(user_data)
            continue

        # Convert the "Investing Amount" to a float after ensuring it is not empty
        initial_amount = float(user_data["Investing Amount"])
        initial_balance = balance

        # Check the order status and get the new amount using the appropriate function
        check_order_status(user_data)

        # Calculate the profit/loss after updating the investment
        new_amount = user_data["new_amount"]
        if new_amount:
            profit_or_loss = float(new_amount) - initial_amount

            # Check if there is any profit/loss and update the investment_changes list
            if profit_or_loss != 0:
                investment_changes.append({
                    "Name": user_data["Name"],
                    "Anime Title": user_data["Anime Title"],
                    "Investment Type": user_data["Investment Type"],
                    "Profit/Loss": profit_or_loss
                })

    return investment_changes


# Function to remove all user investments from the CSV file
def reset_user_investments():
    with open(user_investment_csv, 'r', newline='') as csvfile:
        reader = csv.reader(csvfile)
        headers = next(reader)  # Read the header row
    
    with open(user_investment_csv, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(headers)  # Write the header row back to the file


# Schedule the update_user_investments function to run every 10 minutes
scheduler.add_job(update_user_investments, 'interval', minutes=10)
    
@app.route("/")
def index():
    return render_template("index.html", anime_data_list=anime_data_list)

@app.route('/search', methods=['GET'])
def search():
    search_query = request.args.get('search')

    # Implement your search logic here, for example using difflib:
    matches = difflib.get_close_matches(search_query.lower(), [anime_data['title'].lower() for anime_data in anime_data_list], cutoff=0.6)
    alternative_matches = []
    for anime_data in anime_data_list:
        if 'alternative_titles' in anime_data:
            alternative_titles = anime_data['alternative_titles']
            for key, value in alternative_titles.items():
                if isinstance(value, list):
                    for alt_title in value:
                        if search_query.lower() in alt_title.lower():
                            alternative_matches.append(anime_data)
                            break
                elif isinstance(value, str) and search_query.lower() in value.lower():
                    alternative_matches.append(anime_data)
                    break

    # Combine the matches from both the main titles and alternative titles
    all_matches = matches + alternative_matches

    # Extract the anime IDs from the search results
    anime_ids = [anime_data['id'] for anime_data in all_matches]

    # Redirect to the first anime result page if available
    if anime_ids:
        return redirect(url_for('show_results', anime_id=anime_ids[0]))
    else:
        # If no search results, you can handle this case as needed
        return "No results found."


@app.route("/results/<int:anime_id>")
def show_results(anime_id):
    anime_title, mean_score = get_anime_data(anime_id)
    if not anime_title or mean_score is None:
        return "Anime data not found."

    fig = plot_line_chart(anime_id)
    graph_json = fig.to_json()

    # Pass the specific anime details to the results.html template
    return render_template("results.html", anime_title=anime_title, anime_id=anime_id, mean_score=mean_score, graph_json=graph_json)


@app.route("/buy_high", methods=["POST"])
def buy_high():
    global balance

    name = request.form.get("name")
    anime_id = int(request.form.get("anime_id"))
    anime_title = request.form.get("anime_title")
    investing_amount = float(request.form.get("investing_amount"))
    
    # Get the mean score using the get_mean_score function
    mean_score = get_mean_score(anime_id)
    # Calculate PL Multiplier based on the anime_id
    pl_multiplier = p_multiplicator_generator(anime_id)

   # Convert the target and limiter to float (assuming they are numeric inputs)
    try:
        target = float(request.form.get("target"))
        limiter = request.form.get("limiter")
    except ValueError:
        # Show an error message using JavaScript alert
        error_message = "Invalid input for target or limiter"
        anime_title, mean_score = get_anime_data(anime_id)
        fig = plot_line_chart(anime_id)
        graph_json = fig.to_json()
        return render_template("results.html", anime_title=anime_title, anime_id=anime_id, mean_score=mean_score, graph_json=graph_json, error_message=error_message)

    # Check the conditions for target and limiter
    if target <= mean_score or (limiter and float(limiter) >= mean_score):
        # Show an error message using JavaScript alert
        error_message = "Target must be greater than the mean score, and Limiter must be less than the mean score"
        anime_title, mean_score = get_anime_data(anime_id)
        fig = plot_line_chart(anime_id)
        graph_json = fig.to_json()
        return render_template("results.html", anime_title=anime_title, anime_id=anime_id, mean_score=mean_score, graph_json=graph_json, error_message=error_message)

   # Retrieve the checkbox values from the form
    intraday = bool(request.form.get("intraday"))
    days15 = bool(request.form.get("days15"))
    month1 = bool(request.form.get("month1"))
    month3 = bool(request.form.get("month3"))
# Create a list to store user investment data for different durations
    user_investment_list = []

    # Calculate the start and end dates based on checkbox values
    current_date = datetime.now()
    start_date = current_date.strftime("%d-%m-%Y")
    if intraday:
        # For Intraday, set the end date to next day (24 hrs later)
        end_date = (current_date + timedelta(days=1)).strftime("%d-%m-%Y")
        # Create user investment data for Intraday duration and add to the list
        user_data_intraday = {
            "Investment Type": "BUY(HIGH)",
            "Anime ID": anime_id,
            "Anime Title": anime_title,
            "Name": name,
            "UPDATED Score": mean_score,
            "Start Date": start_date,
            "End Date": end_date,
            "Target": target,
            "Limiter": limiter,
            "Investing Amount": investing_amount,
            "PL Multiplier": pl_multiplier
        }
        user_investment_list.append(user_data_intraday)

    if days15:
        # For 15 Days, set the end date to 15 days later
        end_date = (current_date + timedelta(days=15)).strftime("%d-%m-%Y")
        # Create user investment data for 15 Days duration and add to the list
        user_data_days15 = {
            "Investment Type": "BUY(HIGH)",
            "Anime ID": anime_id,
            "Anime Title": anime_title,
            "Name": name,
            "UPDATED Score": mean_score,
            "Start Date": start_date,
            "End Date": end_date,
            "Target": target,
            "Limiter": limiter,
            "Investing Amount": investing_amount,
            "PL Multiplier": pl_multiplier
        }
        user_investment_list.append(user_data_days15)

    if month1:
        # For 1 Month, set the end date to 1 month later
        end_date = (current_date + timedelta(days=30)).strftime("%d-%m-%Y")
        # Create user investment data for 1 Month duration and add to the list
        user_data_month1 = {
            "Investment Type": "BUY(HIGH)",
            "Anime ID": anime_id,
            "Anime Title": anime_title,
            "Name": name,
            "UPDATED Score": mean_score,
            "Start Date": start_date,
            "End Date": end_date,
            "Target": target,
            "Limiter": limiter,
            "Investing Amount": investing_amount,
            "PL Multiplier": pl_multiplier
        }
        user_investment_list.append(user_data_month1)

    if month3:
        # For 3 Months, set the end date to 3 months later
        end_date = (current_date + timedelta(days=90)).strftime("%d-%m-%Y")
        # Create user investment data for 3 Months duration and add to the list
        user_data_month3 = {
            "Investment Type": "BUY(HIGH)",
            "Anime ID": anime_id,
            "Anime Title": anime_title,
            "Name": name,
            "UPDATED Score": mean_score,
            "Start Date": start_date,
            "End Date": end_date,
            "Target": target,
            "Limiter": limiter,
            "Investing Amount": investing_amount,
            "PL Multiplier": pl_multiplier
        }
        user_investment_list.append(user_data_month3)
# Deduct the investing amount from the current balance for each order
    current_balance = balance
    for user_data in user_investment_list:
        if current_balance >= user_data["Investing Amount"]:
            current_balance -= user_data["Investing Amount"]
        else:
            # Show an error message using JavaScript alert if the balance is not sufficient
            error_message = "Insufficient balance for the investment amount."
            anime_title, mean_score = get_anime_data(anime_id)
            fig = plot_line_chart(anime_id)
            graph_json = fig.to_json()
            return render_template("results.html", anime_title=anime_title, anime_id=anime_id, mean_score=mean_score, graph_json=graph_json, error_message=error_message)

    # Update the global balance with the updated current_balance
    balance = current_balance

    # Write the user investment data to the user_investment.csv file
    write_to_user_investment_csv(user_investment_csv, user_investment_list)

    return render_template("buy_success.html")


@app.route("/buy_low", methods=["POST"])
def buy_low():
    global balance

    name = request.form.get("name")
    anime_id = int(request.form.get("anime_id"))
    anime_title = request.form.get("anime_title")
    investing_amount = float(request.form.get("investing_amount"))

    # Get the mean score using the get_mean_score function
    mean_score = get_mean_score(anime_id)
    # Calculate PL Multiplier based on the anime_id
    pl_multiplier = p_multiplicator_generator(anime_id)

    # Convert the target and limiter to float (assuming they are numeric inputs)
    try:
        target = float(request.form.get("target"))
        limiter = request.form.get("limiter")
    except ValueError:
        # Show an error message using JavaScript alert
        error_message = "Invalid input for target or limiter"
        anime_title, mean_score = get_anime_data(anime_id)
        fig = plot_line_chart(anime_id)
        graph_json = fig.to_json()
        return render_template("results.html", anime_title=anime_title, anime_id=anime_id, mean_score=mean_score, graph_json=graph_json, error_message=error_message)

    # Check the conditions for target and limiter
    if target >= mean_score or (limiter and float(limiter) <= mean_score):
        # Show an error message using JavaScript alert
        error_message = "Target must be less than the mean score, and Limiter must be greater than the mean score"
        anime_title, mean_score = get_anime_data(anime_id)
        fig = plot_line_chart(anime_id)
        graph_json = fig.to_json()
        return render_template("results.html", anime_title=anime_title, anime_id=anime_id, mean_score=mean_score, graph_json=graph_json, error_message=error_message)

    # Retrieve the checkbox values from the form
    intraday = bool(request.form.get("intraday"))
    days15 = bool(request.form.get("days15"))
    month1 = bool(request.form.get("month1"))
    month3 = bool(request.form.get("month3"))

    # Create a list to store user investment data for different durations
    user_investment_list = []

    # Calculate the start and end dates based on checkbox values
    current_date = datetime.now()
    start_date = current_date.strftime("%d-%m-%Y")
    if intraday:
        # For Intraday, set the end date to next day (24 hrs later)
        end_date = (current_date + timedelta(days=1)).strftime("%d-%m-%Y")
        # Create user investment data for Intraday duration and add to the list
        user_data_intraday = {
            "Investment Type": "BUY(LOW)",
            "Anime ID": anime_id,
            "Anime Title": anime_title,
            "Name": name,
            "UPDATED Score": mean_score,
            "Start Date": start_date,
            "End Date": end_date,
            "Target": target,
            "Limiter": limiter,
            "Investing Amount": investing_amount,
            "PL Multiplier": pl_multiplier
        }
        user_investment_list.append(user_data_intraday)

    if days15:
        # For 15 Days, set the end date to 15 days later
        end_date = (current_date + timedelta(days=15)).strftime("%d-%m-%Y")
        # Create user investment data for 15 Days duration and add to the list
        user_data_days15 = {
            "Investment Type": "BUY(LOW)",
            "Anime ID": anime_id,
            "Anime Title": anime_title,
            "Name": name,
            "UPDATED Score": mean_score,
            "Start Date": start_date,
            "End Date": end_date,
            "Target": target,
            "Limiter": limiter,
            "Investing Amount": investing_amount,
            "PL Multiplier": pl_multiplier
        }
        user_investment_list.append(user_data_days15)

    if month1:
        # For 1 Month, set the end date to 1 month later
        end_date = (current_date + timedelta(days=30)).strftime("%d-%m-%Y")
        # Create user investment data for 1 Month duration and add to the list
        user_data_month1 = {
            "Investment Type": "BUY(LOW)",
            "Anime ID": anime_id,
            "Anime Title": anime_title,
            "Name": name,
            "UPDATED Score": mean_score,
            "Start Date": start_date,
            "End Date": end_date,
            "Target": target,
            "Limiter": limiter,
            "Investing Amount": investing_amount,
            "PL Multiplier": pl_multiplier
        }
        user_investment_list.append(user_data_month1)

    if month3:
        # For 3 Months, set the end date to 3 months later
        end_date = (current_date + timedelta(days=90)).strftime("%d-%m-%Y")
        # Create user investment data for 3 Months duration and add to the list
        user_data_month3 = {
            "Investment Type": "BUY(LOW)",
            "Anime ID": anime_id,
            "Anime Title": anime_title,
            "Name": name,
            "UPDATED Score": mean_score,
            "Start Date": start_date,
            "End Date": end_date,
            "Target": target,
            "Limiter": limiter,
            "Investing Amount": investing_amount,
            "PL Multiplier": pl_multiplier
        }
        user_investment_list.append(user_data_month3)

    # Deduct the investing amount from the current balance for each order
    current_balance = balance
    for user_data in user_investment_list:
        if current_balance >= user_data["Investing Amount"]:
            current_balance -= user_data["Investing Amount"]
        else:
            # Show an error message using JavaScript alert if the balance is not sufficient
            error_message = "Insufficient balance for the investment amount."
            anime_title, mean_score = get_anime_data(anime_id)
            fig = plot_line_chart(anime_id)
            graph_json = fig.to_json()
            return render_template("results.html", anime_title=anime_title, anime_id=anime_id, mean_score=mean_score, graph_json=graph_json, error_message=error_message)

    # Update the global balance with the updated current_balance
    balance = current_balance

    # Write the user investment data to the user_investment.csv file
    write_to_user_investment_csv(user_investment_csv, user_investment_list)

    return render_template("buy_success.html")

@app.route("/reset", methods=["POST"])
def reset_investments():
    global balance
    # Reset the balance to the initial value
    balance = 10000
    # Reset all user investments from the CSV file
    reset_user_investments()
    # Redirect to the user investment page after reset
    return redirect(url_for("user_investment"))

# Route for displaying the user investment data from the CSV file
@app.route('/user_investment')
def user_investment():
    user_investments = fetch_user_investments()
    investment_changes = update_user_investments()
    return render_template('user_investment.html', user_investments=user_investments, investment_changes=investment_changes)



@app.route("/success")
def success():
    return render_template("buy_success.html")




@app.route('/broadcast', methods=['GET'])
def broadcast_sort():
    sorted_anime_data = sorted(anime_data_list, key=lambda x: x["broadcast"])
    return render_template('index.html', anime_data_list=sorted_anime_data)


# Route for displaying the balance
@app.route('/balance')
def balance_page():
    global balance
    return render_template('balance.html', balance_amount=balance)

if __name__ == "__main__":
    scheduler.start()
    app.run(debug=True)
