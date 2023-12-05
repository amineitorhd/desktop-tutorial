import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from random import choice


window=tk.Tk()
window.title("filtrageAnimé")
window.geometry("600x400")

frame=ttk.Frame(window)
cv=tk.Canvas(frame,bg="magenta")
cv.pack(fill="both",expand=1)


dico2={'Number': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132, 133, 134, 135, 136, 137, 138, 139, 140, 141, 142, 143, 144, 145, 146, 147, 148, 149, 150, 151, 152, 153, 154, 155, 156, 157, 158, 159, 160, 161, 162, 163, 164, 165, 166, 167, 168, 169, 170, 171, 172, 173, 174, 175, 176, 177, 178, 179, 180, 181, 182, 183, 184, 185, 186, 187, 188, 189, 190, 191, 192, 193, 194, 195, 196, 197, 198, 199, 200, 201, 202, 203, 204, 205, 206, 207, 208, 209, 210, 211, 212, 213, 214, 215, 216, 217, 218, 219, 220, 221, 222, 223, 224, 225, 226, 227, 228, 229, 230, 231, 232, 233, 234, 235, 236, 237, 238, 239, 240, 241, 242, 243, 244, 245, 246, 247, 248, 249, 250, 251, 252, 253, 254, 255, 256, 257, 258, 259, 260, 261, 262, 263, 264, 265, 266, 267, 268, 269, 270, 271, 272, 273, 274, 275, 276, 277, 278, 279, 280, 281, 282, 283, 284, 285, 286, 287, 288, 289, 290, 291, 292, 293, 294, 295, 296, 297, 298, 299, 300, 301, 302, 303, 304, 305, 306, 307, 308, 309, 310, 311, 312, 313, 314, 315, 316, 317, 318, 319, 320, 321, 322, 323, 324, 325, 326, 327, 328, 329, 330, 331, 332, 333, 334, 335, 336, 337, 338, 339, 340, 341, 342, 343, 344, 345, 346, 347, 348, 349, 350, 351, 352, 353, 354, 355, 356, 357, 358, 359, 360, 361, 362, 363, 364, 365, 366, 367, 368, 369, 370, 371, 372, 373, 374, 375, 376, 377, 378, 379, 380, 381, 382, 383, 384, 385, 386, 387, 388, 389, 390, 391, 392, 393, 394, 395, 396, 397, 398, 399, 400, 401, 402, 403, 404, 405, 406, 407, 408, 409, 410, 411, 412, 413, 414, 415, 416, 417, 418, 419, 420, 421, 422, 423, 424, 425, 426, 427, 428, 429, 430, 431, 432, 433, 434, 435, 436, 437, 438, 439, 440, 441, 442, 443, 444, 445, 446, 447, 448, 449, 450, 451, 452, 453, 454, 455, 456, 457, 458, 459, 460, 461, 462, 463, 464, 465, 466, 467, 468, 469, 470, 471, 472, 473, 474, 475, 476, 477, 478, 479, 480, 481, 482, 483, 484, 485, 486, 487, 488, 489, 490, 491, 492, 493, 494, 495, 496, 497, 498, 499, 500, 501, 502, 503, 504, 505, 506, 507, 508, 509, 510, 511, 512, 513, 514, 515, 516, 517, 518, 519, 520, 521, 522, 523, 524, 525, 526, 527, 528, 529, 530, 531, 532, 533, 534, 535, 536, 537, 538, 539, 540, 541, 542, 543, 544, 545, 546, 547, 548, 549, 550, 551, 552, 553, 554, 555, 556, 557, 558, 559, 560, 561, 562, 563, 564, 565, 566, 567, 568, 569, 570, 571, 572, 573, 574, 575, 576, 577, 578, 579, 580, 581, 582, 583, 584, 585, 586, 587, 588, 589, 590, 591, 592, 593, 594, 595, 596, 597, 598, 599, 600, 601, 602, 603, 604, 605, 606, 607, 608, 609, 610, 611, 612, 613, 614, 615, 616, 617, 618, 619, 620, 621, 622, 623, 624, 625, 626, 627, 628, 629, 630, 631, 632, 633, 634, 635, 636, 637, 638, 639, 640, 641, 642, 643, 644, 645, 646, 647, 648, 649, 650, 651, 652, 653, 654, 655, 656, 657, 658, 659, 660, 661, 662, 663, 664, 665, 666, 667, 668, 669, 670, 671, 672, 673, 674, 675, 676, 677, 678, 679, 680, 681, 682, 683, 684, 685, 686, 687, 688, 689, 690, 691, 692, 693, 694, 695, 696, 697, 698, 699, 700, 701, 702, 703, 704, 705, 706, 707, 708, 709, 710, 711, 712, 713, 714, 715, 716, 717, 718, 719, 720, 721], 'Name': ['Bulbasaur', 'Ivysaur', 'Venusaur', 'VenusaurMega Venusaur', 'Charmander', 'Charmeleon', 'Charizard', 'CharizardMega Charizard X', 'CharizardMega Charizard Y', 'Squirtle', 'Wartortle', 'Blastoise', 'BlastoiseMega Blastoise', 'Caterpie', 'Metapod', 'Butterfree', 'Weedle', 'Kakuna', 'Beedrill', 'BeedrillMega Beedrill', 'Pidgey', 'Pidgeotto', 'Pidgeot', 'PidgeotMega Pidgeot', 'Rattata', 'Raticate', 'Spearow', 'Fearow', 'Ekans', 'Arbok', 'Pikachu', 'Raichu', 'Sandshrew', 'Sandslash', 'Nidoran♀', 'Nidorina', 'Nidoqueen', 'Nidoran♂', 'Nidorino', 'Nidoking', 'Clefairy', 'Clefable', 'Vulpix', 'Ninetales', 'Jigglypuff', 'Wigglytuff', 'Zubat', 'Golbat', 'Oddish', 'Gloom', 'Vileplume', 'Paras', 'Parasect', 'Venonat', 'Venomoth', 'Diglett', 'Dugtrio', 'Meowth', 'Persian', 'Psyduck', 'Golduck', 'Mankey', 'Primeape', 'Growlithe', 'Arcanine', 'Poliwag', 'Poliwhirl', 'Poliwrath', 'Abra', 'Kadabra', 'Alakazam', 'AlakazamMega Alakazam', 'Machop', 'Machoke', 'Machamp', 'Bellsprout', 'Weepinbell', 'Victreebel', 'Tentacool', 'Tentacruel', 'Geodude', 'Graveler', 'Golem', 'Ponyta', 'Rapidash', 'Slowpoke', 'Slowbro', 'SlowbroMega Slowbro', 'Magnemite', 'Magneton', "Farfetch'd", 'Doduo', 'Dodrio', 'Seel', 'Dewgong', 'Grimer', 'Muk', 'Shellder', 'Cloyster', 'Gastly', 'Haunter', 'Gengar', 'GengarMega Gengar', 'Onix', 'Drowzee', 'Hypno', 'Krabby', 'Kingler', 'Voltorb', 'Electrode', 'Exeggcute', 'Exeggutor', 'Cubone', 'Marowak', 'Hitmonlee', 'Hitmonchan', 'Lickitung', 'Koffing', 'Weezing', 'Rhyhorn', 'Rhydon', 'Chansey', 'Tangela', 'Kangaskhan', 'KangaskhanMega Kangaskhan', 'Horsea', 'Seadra', 'Goldeen', 'Seaking', 'Staryu', 'Starmie', 'Mr. Mime', 'Scyther', 'Jynx', 'Electabuzz', 'Magmar', 'Pinsir', 'PinsirMega Pinsir', 'Tauros', 'Magikarp', 'Gyarados', 'GyaradosMega Gyarados', 'Lapras', 'Ditto', 'Eevee', 'Vaporeon', 'Jolteon', 'Flareon', 'Porygon', 'Omanyte', 'Omastar', 'Kabuto', 'Kabutops', 'Aerodactyl', 'AerodactylMega Aerodactyl', 'Snorlax', 'Articuno', 'Zapdos', 'Moltres', 'Dratini', 'Dragonair', 'Dragonite', 'Mewtwo', 'MewtwoMega Mewtwo X', 'MewtwoMega Mewtwo Y', 'Mew', 'Chikorita', 'Bayleef', 'Meganium', 'Cyndaquil', 'Quilava', 'Typhlosion', 'Totodile', 'Croconaw', 'Feraligatr', 'Sentret', 'Furret', 'Hoothoot', 'Noctowl', 'Ledyba', 'Ledian', 'Spinarak', 'Ariados', 'Crobat', 'Chinchou', 'Lanturn', 'Pichu', 'Cleffa', 'Igglybuff', 'Togepi', 'Togetic', 'Natu', 'Xatu', 'Mareep', 'Flaaffy', 'Ampharos', 'AmpharosMega Ampharos', 'Bellossom', 'Marill', 'Azumarill', 'Sudowoodo', 'Politoed', 'Hoppip', 'Skiploom', 'Jumpluff', 'Aipom', 'Sunkern', 'Sunflora', 'Yanma', 'Wooper', 'Quagsire', 'Espeon', 'Umbreon', 'Murkrow', 'Slowking', 'Misdreavus', 'Unown', 'Wobbuffet', 'Girafarig', 'Pineco', 'Forretress', 'Dunsparce', 'Gligar', 'Steelix', 'SteelixMega Steelix', 'Snubbull', 'Granbull', 'Qwilfish', 'Scizor', 'ScizorMega Scizor', 'Shuckle', 'Heracross', 'HeracrossMega Heracross', 'Sneasel', 'Teddiursa', 'Ursaring', 'Slugma', 'Magcargo', 'Swinub', 'Piloswine', 'Corsola', 'Remoraid', 'Octillery', 'Delibird', 'Mantine', 'Skarmory', 'Houndour', 'Houndoom', 'HoundoomMega Houndoom', 'Kingdra', 'Phanpy', 'Donphan', 'Porygon2', 'Stantler', 'Smeargle', 'Tyrogue', 'Hitmontop', 'Smoochum', 'Elekid', 'Magby', 'Miltank', 'Blissey', 'Raikou', 'Entei', 'Suicune', 'Larvitar', 'Pupitar', 'Tyranitar', 'TyranitarMega Tyranitar', 'Lugia', 'Ho-oh', 'Celebi', 'Treecko', 'Grovyle', 'Sceptile', 'SceptileMega Sceptile', 'Torchic', 'Combusken', 'Blaziken', 'BlazikenMega Blaziken', 'Mudkip', 'Marshtomp', 'Swampert', 'SwampertMega Swampert', 'Poochyena', 'Mightyena', 'Zigzagoon', 'Linoone', 'Wurmple', 'Silcoon', 'Beautifly', 'Cascoon', 'Dustox', 'Lotad', 'Lombre', 'Ludicolo', 'Seedot', 'Nuzleaf', 'Shiftry', 'Taillow', 'Swellow', 'Wingull', 'Pelipper', 'Ralts', 'Kirlia', 'Gardevoir', 'GardevoirMega Gardevoir', 'Surskit', 'Masquerain', 'Shroomish', 'Breloom', 'Slakoth', 'Vigoroth', 'Slaking', 'Nincada', 'Ninjask', 'Shedinja', 'Whismur', 'Loudred', 'Exploud', 'Makuhita', 'Hariyama', 'Azurill', 'Nosepass', 'Skitty', 'Delcatty', 'Sableye', 'SableyeMega Sableye', 'Mawile', 'MawileMega Mawile', 'Aron', 'Lairon', 'Aggron', 'AggronMega Aggron', 'Meditite', 'Medicham', 'MedichamMega Medicham', 'Electrike', 'Manectric', 'ManectricMega Manectric', 'Plusle', 'Minun', 'Volbeat', 'Illumise', 'Roselia', 'Gulpin', 'Swalot', 'Carvanha', 'Sharpedo', 'SharpedoMega Sharpedo', 'Wailmer', 'Wailord', 'Numel', 'Camerupt', 'CameruptMega Camerupt', 'Torkoal', 'Spoink', 'Grumpig', 'Spinda', 'Trapinch', 'Vibrava', 'Flygon', 'Cacnea', 'Cacturne', 'Swablu', 'Altaria', 'AltariaMega Altaria', 'Zangoose', 'Seviper', 'Lunatone', 'Solrock', 'Barboach', 'Whiscash', 'Corphish', 'Crawdaunt', 'Baltoy', 'Claydol', 'Lileep', 'Cradily', 'Anorith', 'Armaldo', 'Feebas', 'Milotic', 'Castform', 'Kecleon', 'Shuppet', 'Banette', 'BanetteMega Banette', 'Duskull', 'Dusclops', 'Tropius', 'Chimecho', 'Absol', 'AbsolMega Absol', 'Wynaut', 'Snorunt', 'Glalie', 'GlalieMega Glalie', 'Spheal', 'Sealeo', 'Walrein', 'Clamperl', 'Huntail', 'Gorebyss', 'Relicanth', 'Luvdisc', 'Bagon', 'Shelgon', 'Salamence', 'SalamenceMega Salamence', 'Beldum', 'Metang', 'Metagross', 'MetagrossMega Metagross', 'Regirock', 'Regice', 'Registeel', 'Latias', 'LatiasMega Latias', 'Latios', 'LatiosMega Latios', 'Kyogre', 'KyogrePrimal Kyogre', 'Groudon', 'GroudonPrimal Groudon', 'Rayquaza', 'RayquazaMega Rayquaza', 'Jirachi', 'DeoxysNormal Forme', 'DeoxysAttack Forme', 'DeoxysDefense Forme', 'DeoxysSpeed Forme', 'Turtwig', 'Grotle', 'Torterra', 'Chimchar', 'Monferno', 'Infernape', 'Piplup', 'Prinplup', 'Empoleon', 'Starly', 'Staravia', 'Staraptor', 'Bidoof', 'Bibarel', 'Kricketot', 'Kricketune', 'Shinx', 'Luxio', 'Luxray', 'Budew', 'Roserade', 'Cranidos', 'Rampardos', 'Shieldon', 'Bastiodon', 'Burmy', 'WormadamPlant Cloak', 'WormadamSandy Cloak', 'WormadamTrash Cloak', 'Mothim', 'Combee', 'Vespiquen', 'Pachirisu', 'Buizel', 'Floatzel', 'Cherubi', 'Cherrim', 'Shellos', 'Gastrodon', 'Ambipom', 'Drifloon', 'Drifblim', 'Buneary', 'Lopunny', 'LopunnyMega Lopunny', 'Mismagius', 'Honchkrow', 'Glameow', 'Purugly', 'Chingling', 'Stunky', 'Skuntank', 'Bronzor', 'Bronzong', 'Bonsly', 'Mime Jr.', 'Happiny', 'Chatot', 'Spiritomb', 'Gible', 'Gabite', 'Garchomp', 'GarchompMega Garchomp', 'Munchlax', 'Riolu', 'Lucario', 'LucarioMega Lucario', 'Hippopotas', 'Hippowdon', 'Skorupi', 'Drapion', 'Croagunk', 'Toxicroak', 'Carnivine', 'Finneon', 'Lumineon', 'Mantyke', 'Snover', 'Abomasnow', 'AbomasnowMega Abomasnow', 'Weavile', 'Magnezone', 'Lickilicky', 'Rhyperior', 'Tangrowth', 'Electivire', 'Magmortar', 'Togekiss', 'Yanmega', 'Leafeon', 'Glaceon', 'Gliscor', 'Mamoswine', 'Porygon-Z', 'Gallade', 'GalladeMega Gallade', 'Probopass', 'Dusknoir', 'Froslass', 'Rotom', 'RotomHeat Rotom', 'RotomWash Rotom', 'RotomFrost Rotom', 'RotomFan Rotom', 'RotomMow Rotom', 'Uxie', 'Mesprit', 'Azelf', 'Dialga', 'Palkia', 'Heatran', 'Regigigas', 'GiratinaAltered Forme', 'GiratinaOrigin Forme', 'Cresselia', 'Phione', 'Manaphy', 'Darkrai', 'ShayminLand Forme', 'ShayminSky Forme', 'Arceus', 'Victini', 'Snivy', 'Servine', 'Serperior', 'Tepig', 'Pignite', 'Emboar', 'Oshawott', 'Dewott', 'Samurott', 'Patrat', 'Watchog', 'Lillipup', 'Herdier', 'Stoutland', 'Purrloin', 'Liepard', 'Pansage', 'Simisage', 'Pansear', 'Simisear', 'Panpour', 'Simipour', 'Munna', 'Musharna', 'Pidove', 'Tranquill', 'Unfezant', 'Blitzle', 'Zebstrika', 'Roggenrola', 'Boldore', 'Gigalith', 'Woobat', 'Swoobat', 'Drilbur', 'Excadrill', 'Audino', 'AudinoMega Audino', 'Timburr', 'Gurdurr', 'Conkeldurr', 'Tympole', 'Palpitoad', 'Seismitoad', 'Throh', 'Sawk', 'Sewaddle', 'Swadloon', 'Leavanny', 'Venipede', 'Whirlipede', 'Scolipede', 'Cottonee', 'Whimsicott', 'Petilil', 'Lilligant', 'Basculin', 'Sandile', 'Krokorok', 'Krookodile', 'Darumaka', 'DarmanitanStandard Mode', 'DarmanitanZen Mode', 'Maractus', 'Dwebble', 'Crustle', 'Scraggy', 'Scrafty', 'Sigilyph', 'Yamask', 'Cofagrigus', 'Tirtouga', 'Carracosta', 'Archen', 'Archeops', 'Trubbish', 'Garbodor', 'Zorua', 'Zoroark', 'Minccino', 'Cinccino', 'Gothita', 'Gothorita', 'Gothitelle', 'Solosis', 'Duosion', 'Reuniclus', 'Ducklett', 'Swanna', 'Vanillite', 'Vanillish', 'Vanilluxe', 'Deerling', 'Sawsbuck', 'Emolga', 'Karrablast', 'Escavalier', 'Foongus', 'Amoonguss', 'Frillish', 'Jellicent', 'Alomomola', 'Joltik', 'Galvantula', 'Ferroseed', 'Ferrothorn', 'Klink', 'Klang', 'Klinklang', 'Tynamo', 'Eelektrik', 'Eelektross', 'Elgyem', 'Beheeyem', 'Litwick', 'Lampent', 'Chandelure', 'Axew', 'Fraxure', 'Haxorus', 'Cubchoo', 'Beartic', 'Cryogonal', 'Shelmet', 'Accelgor', 'Stunfisk', 'Mienfoo', 'Mienshao', 'Druddigon', 'Golett', 'Golurk', 'Pawniard', 'Bisharp', 'Bouffalant', 'Rufflet', 'Braviary', 'Vullaby', 'Mandibuzz', 'Heatmor', 'Durant', 'Deino', 'Zweilous', 'Hydreigon', 'Larvesta', 'Volcarona', 'Cobalion', 'Terrakion', 'Virizion', 'TornadusIncarnate Forme', 'TornadusTherian Forme', 'ThundurusIncarnate Forme', 'ThundurusTherian Forme', 'Reshiram', 'Zekrom', 'LandorusIncarnate Forme', 'LandorusTherian Forme', 'Kyurem', 'KyuremBlack Kyurem', 'KyuremWhite Kyurem', 'KeldeoOrdinary Forme', 'KeldeoResolute Forme', 'MeloettaAria Forme', 'MeloettaPirouette Forme', 'Genesect', 'Chespin', 'Quilladin', 'Chesnaught', 'Fennekin', 'Braixen', 'Delphox', 'Froakie', 'Frogadier', 'Greninja', 'Bunnelby', 'Diggersby', 'Fletchling', 'Fletchinder', 'Talonflame', 'Scatterbug', 'Spewpa', 'Vivillon', 'Litleo', 'Pyroar', 'Flabébé', 'Floette', 'Florges', 'Skiddo', 'Gogoat', 'Pancham', 'Pangoro', 'Furfrou', 'Espurr', 'MeowsticMale', 'MeowsticFemale', 'Honedge', 'Doublade', 'AegislashBlade Forme', 'AegislashShield Forme', 'Spritzee', 'Aromatisse', 'Swirlix', 'Slurpuff', 'Inkay', 'Malamar', 'Binacle', 'Barbaracle', 'Skrelp', 'Dragalge', 'Clauncher', 'Clawitzer', 'Helioptile', 'Heliolisk', 'Tyrunt', 'Tyrantrum', 'Amaura', 'Aurorus', 'Sylveon', 'Hawlucha', 'Dedenne', 'Carbink', 'Goomy', 'Sliggoo', 'Goodra', 'Klefki', 'Phantump', 'Treve""t', 'PumpkabooAverage Size', 'PumpkabooSmall Size', 'PumpkabooLarge Size', 'PumpkabooSuper Size', 'GourgeistAverage Size', 'GourgeistSmall Size', 'GourgeistLarge Size', 'GourgeistSuper Size', 'Bergmite', 'Avalugg', 'Noibat', 'Noivern', 'Xerneas', 'Yveltal', 'Zygarde50% Forme', 'Diancie', 'DiancieMega Diancie', 'HoopaHoopa Confined', 'HoopaHoopa Unbound', 'Volcanion'], 'Type_1': ['Grass', 'Fire', 'Water', 'Bug', 'Normal', 'Poison', 'Electric', 'Ground', 'Fairy', 'Fighting', 'Psychic', 'Rock', 'Ghost', 'Ice', 'Dragon', 'Dark', 'Steel', 'Flying'], 'Type_2': ['Poison', "", 'Flying', 'Dragon', 'Ground', 'Fairy', 'Grass', 'Fighting', 'Psychic', 'Steel', 'Ice', 'Rock', 'Dark', 'Water', 'Electric', 'Fire', 'Ghost', 'Bug', 'Normal'], 'Total': [318, 405, 525, 625, 309, 534, 634, 314, 530, 630, 195, 205, 395, 495, 251, 349, 479, 579, 253, 413, 262, 442, 288, 438, 320, 485, 300, 450, 275, 365, 505, 273, 323, 483, 299, 270, 435, 245, 455, 490, 285, 305, 265, 290, 440, 500, 350, 555, 385, 510, 310, 400, 590, 390, 335, 515, 410, 315, 325, 465, 352, 460, 475, 600, 328, 330, 480, 520, 425, 340, 345, 295, 200, 540, 640, 535, 355, 615, 580, 420, 680, 780, 215, 415, 250, 218, 210, 470, 280, 610, 360, 180, 430, 336, 380, 700, 635, 220, 240, 198, 278, 518, 618, 269, 414, 670, 266, 456, 236, 237, 474, 190, 375, 260, 575, 302, 467, 560, 458, 468, 308, 565, 770, 194, 384, 263, 363, 523, 224, 424, 244, 482, 348, 498, 452, 329, 411, 454, 334, 494, 594, 545, 720, 528, 418, 255, 370, 281, 446, 316, 292, 487, 264, 358, 488, 497, 313, 508, 445, 294, 509, 351, 519, 461, 303, 401, 567, 473, 428, 464, 319, 472, 489, 471, 484, 550, 660, 307, 409, 423, 382, 499, 213, 369, 507, 371, 552, 531, 466, 448, 341, 462, 306, 289, 481, 362, 521, 431, 304, 514], 'HP': [45, 60, 80, 39, 58, 78, 44, 59, 79, 50, 40, 65, 63, 83, 30, 55, 35, 75, 70, 90, 46, 61, 81, 95, 38, 73, 115, 140, 10, 25, 52, 105, 85, 250, 20, 130, 48, 160, 41, 91, 106, 100, 125, 190, 255, 28, 68, 150, 31, 1, 64, 84, 104, 72, 144, 170, 110, 43, 66, 86, 99, 76, 53, 37, 77, 67, 97, 111, 49, 71, 103, 57, 108, 135, 74, 69, 120, 116, 62, 54, 36, 51, 114, 165, 109, 89, 92, 56, 88, 123, 101, 82, 42, 126], 'Attack': [49, 62, 82, 100, 52, 64, 84, 130, 104, 48, 63, 83, 103, 30, 20, 45, 35, 25, 90, 150, 60, 80, 56, 81, 85, 55, 75, 47, 92, 57, 72, 102, 70, 41, 76, 50, 65, 95, 105, 110, 40, 120, 73, 5, 125, 67, 155, 10, 115, 135, 134, 190, 46, 38, 58, 33, 185, 164, 160, 51, 71, 91, 140, 43, 78, 15, 165, 68, 23, 145, 180, 89, 109, 66, 86, 42, 29, 59, 79, 69, 94, 136, 93, 24, 170, 112, 61, 106, 132, 123, 88, 53, 98, 77, 27, 117, 108, 44, 87, 147, 74, 124, 97, 129, 128, 107, 36, 22, 54, 121, 131], 'Defense': [49, 63, 83, 123, 43, 58, 78, 111, 65, 80, 100, 120, 35, 55, 50, 30, 40, 75, 60, 44, 69, 85, 110, 52, 67, 87, 57, 77, 48, 73, 20, 45, 70, 25, 95, 15, 115, 130, 180, 160, 90, 53, 79, 5, 109, 125, 105, 64, 34, 38, 28, 42, 140, 200, 230, 62, 37, 10, 150, 41, 61, 32, 23, 135, 97, 71, 68, 88, 51, 118, 168, 102, 66, 84, 94, 47, 86, 116, 108, 72, 56, 76, 145, 107, 106, 39, 126, 59, 99, 89, 103, 133, 82, 91, 131, 112, 129, 122, 54, 33, 119, 184, 121], 'Sp_Atk': [65, 80, 100, 122, 60, 109, 130, 159, 50, 85, 135, 20, 25, 90, 45, 15, 35, 70, 31, 61, 40, 55, 75, 95, 81, 30, 110, 105, 120, 175, 58, 115, 170, 43, 73, 125, 48, 154, 194, 49, 63, 83, 44, 59, 79, 36, 76, 56, 165, 72, 33, 10, 140, 145, 51, 71, 91, 47, 46, 93, 23, 74, 94, 114, 160, 150, 180, 78, 104, 111, 42, 29, 69, 62, 87, 57, 92, 54, 64, 41, 24, 38, 68, 86, 132, 116, 108, 88, 53, 98, 67, 107, 77, 37, 106, 103, 112, 97, 129, 128, 32, 27, 99, 39, 131], 'Sp_Def': [65, 80, 100, 120, 50, 85, 115, 64, 105, 20, 25, 35, 70, 31, 61, 54, 79, 30, 55, 40, 75, 90, 45, 95, 60, 62, 110, 130, 48, 125, 63, 83, 56, 96, 76, 42, 58, 230, 140, 135, 154, 41, 52, 82, 23, 43, 73, 53, 71, 87, 107, 33, 200, 150, 160, 44, 101, 51, 34, 49, 88, 138, 102, 78, 66, 37, 59, 86, 116, 108, 72, 77, 106, 39, 69, 32, 126, 67, 99, 129, 128, 36, 38, 98, 57, 81, 89, 46, 123, 94, 92, 113], 'Speed': [45, 60, 80, 65, 100, 43, 58, 78, 30, 70, 50, 35, 75, 145, 56, 71, 101, 121, 72, 97, 55, 90, 110, 40, 41, 76, 85, 20, 25, 95, 120, 115, 105, 150, 15, 130, 42, 67, 140, 87, 63, 68, 93, 81, 48, 91, 33, 5, 83, 51, 61, 125, 160, 28, 135, 10, 23, 32, 52, 180, 31, 36, 108, 66, 34, 39, 112, 74, 84, 82, 102, 92, 47, 46, 86, 77, 127, 113, 106, 64, 24, 29, 116, 114, 88, 69, 57, 98, 22, 44, 59, 79, 103, 109, 38, 111, 128, 99, 73, 104, 122, 62, 126, 89, 49, 118, 54, 123], 'Generation': [1, 2, 3, 4, 5, 6], 'Legendary': [False, True]}

dico={'Number': (True, 'Id_Type'), 'Name': (False, 'Id_Type'), 'Type_2': (False, 'type'), 'Total': (True, 'BatailleStat_Type'), 'HP': (True, 'BatailleStat_Type'), 'Attack': (True, 'BatailleStat_Type'), 'Defense': (True, 'BatailleStat_Type'), 'Sp_Atk': (True, 'BatailleStat_Type'), 'Sp_Def': (True, 'BatailleStat_Type'), 'Speed': (True, 'BatailleStat_Type'), 'Generation': (True, 'Categorique_Type'), 'Legendary': (False, 'Booleen_Type')}
cv.columnconfigure((0,1,2,3),weight=1,uniform="a")
cv.rowconfigure((0,1,2,3),weight=1,uniform="a")

FrameBataille=ttk.Frame(cv)

FrameType=ttk.Frame(cv)
frame_gauche=ttk.Frame(FrameType)
frame_droite=ttk.Frame(FrameType)
frame_gauche.pack(side="left")
frame_droite.pack(side="right")
FrameLegend=ttk.Frame(cv)
FrameGeneration=ttk.Frame(cv)


#or valeur[1]=="type" or valeur[1]=='Booleen_Type':
k=0
for cle,valeur in dico.items():
    
    if valeur[1]=="Categorique_Type":
        titre=ttk.Label(FrameGeneration,text=cle)
        titre.pack()
        for valeur in dico2[cle]:
            bouton=ttk.Button(FrameGeneration,text=valeur)
            bouton.pack(side="left")
    elif valeur[1]=="type":
        titre=ttk.Label(FrameType,text=cle)
        titre.pack(side="top")
        for valeur in dico2[cle]:
            if k<10:
                k+=1
                bouton=ttk.Button(frame_gauche,text=valeur)
                bouton.pack(anchor="nw")
            else:
                bouton=ttk.Button(frame_droite,text=valeur)
                bouton.pack(anchor="nw")
    elif valeur[1]=="BatailleStat_Type":
        titre=ttk.Label(FrameBataille,text=f"¨{cle}")
        titre.pack(side="top",pady=10)
        barre=ttk.Scale(FrameBataille,orient="horizontal")
        barre.pack()
    elif valeur[1]=='Booleen_Type':
        titre=ttk.Label(FrameLegend,text=cle)
        titre.pack(side="top")
        for valeur in dico2[cle]:
            bouton=ttk.Button(FrameLegend,text=valeur)
            bouton.pack(side="left")


# FrameBataille.place(relx=0.05,relwidth=0.35,rely=0.6,relheight=0.7)
FrameBataille.place(relx=0.6,relwidth=0.15,rely=0.05,relheight=0.7)

FrameGeneration.place(relx=0.5,relwidth=0.45,rely=0.8,relheight=0.15)

FrameType.place(relx=0.05,relwidth=0.15,rely=0.05,relheight=0.7)

# FrameLegend.place(relx=0.8,relwidth=0.3,rely=0.05,relheight=0.15)
FrameLegend.place(relx=0.05,relwidth=0.3,rely=0.8,relheight=0.15)


window.mainloop()



# window.mainloop()