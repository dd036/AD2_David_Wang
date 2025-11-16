import random

class Pokemon:
    def __init__(self, nombre, hp, ataque):
        self.nombre = nombre
        self.hp = hp
        self.ataque = ataque
        self.hp_actual = hp
    def curar (self):
        self.hp_actual = self.hp
    def cambio_stats(self):
        self.hp = round(self.hp * 1.1, 2)
        self.ataque = round(self.ataque * 1.1, 2)
        self.curar
        print(f"{self.nombre} ha subido de nivel, sus nuevos stats son:\n"
              f"{self.ataque} ataque\n"
              f"{self.hp} max HP")

class Tipo(Pokemon):

    def __init__(self, nombre, tipo, hp, ataque):
        super().__init__(nombre, hp, ataque)
        self.tipo = tipo
        self.nivel = 0
    
    #diccionario de la tabla de Tipos
    tabla_tipo_fuerte = {
    "fuego": ["planta", "bicho"],
    "planta": ["agua", "tierra", "roca"],
    "agua": ["fuego", "tierra", "roca"],
    "electrico": ["agua", "volador"],
    "hielo": ["planta", "tierra", "volador", "dragon"],
    "lucha": ["normal", "hielo", "roca"],
    "veneno": ["planta"],
    "tierra": ["roca", "electrico", "veneno", "fuego"],
    "volador": ["lucha", "planta", "bicho"],
    "psiquico": ["lucha", "veneno"],
    "bicho": ["planta", "psiquico"],
    "roca": ["volador", "fuego", "hielo", "bicho"],
    "fantasma": ["fantasma"],
    "dragon": ["dragon"]
    }
    def atacar (self, otro):
        #tabla de Tipos
        multiplicador = 1.5 if otro.tipo in Tipo.tabla_tipo_fuerte.get(self.tipo, []) else 1.0
        daño = self.ataque * multiplicador
        otro.hp_actual = otro.hp_actual - daño 
        if otro.hp_actual < 0:
            otro.hp_actual = 0
        return daño

    def posible_captura(self):
        if self.hp >= self.hp_actual >= self.hp*0.75:
            porcentage = 0.33
        elif 0.75*self.hp >= self.hp_actual > self.hp*0.5:
            porcentage = 0.5
        else:
            porcentage = 0.75
        return porcentage
        
class Boss(Tipo):
    def __init__(self, nombre, tipo, hp, ataque):
        super().__init__(nombre, tipo, hp, ataque)

    def final_form(self):
        self.hp_actual += self.hp/4
        self.ataque *= 1.3

class Equipo:
    def __init__(self):
        self.dinero = 0
        self.pokemons = {
            "slot 1": None,
            "slot 2": None,
            "slot 3": None,
            "slot 4": None,
            "slot 5": None,
            "slot 6": None
        }
        self.evo_index = {
            "slot 1": 0,
            "slot 2": 0,
            "slot 3": 0,
            "slot 4": 0,
            "slot 5": 0,
            "slot 6": 0,
        }
    
    def agregar_pokemon(self, pokemon):
        no_capturado = True
        for i in range(2,7):
            slot_capturado = f"slot {i}"
            if no_capturado == True:
                if self.pokemons[slot_capturado] is None:
                    self.pokemons[slot_capturado] = pokemon
                    no_capturado = False
                    

        if no_capturado:
            print("tu equipo está lleno y no puedes capturar más pokemons")
        return no_capturado

    def ver_equipo(self):
        print("tu equipo esta formado por:")
        for key, value in self.pokemons.items():
            if value is not None:
                idx = self.evo_index[key]
                poke = value[idx]
                print(f"{key}: {poke.nombre} (Nv {poke.nivel}, HP {round(poke.hp_actual,2)}/{poke.hp})")
            else:
                print(f"{key}: vacio")

    def regenerar(self, pokemon_curar):
        if pokemon_curar.hp == pokemon_curar.hp_actual:
            print("ese pokemon tiene full HP")
            return 
        if self.dinero < 100:
            print("no tienes suficiente dinero")
            return 
        
        confirmacion = input("la curacion va a costar 100 de oro por pokemon, quieres continuar? \nsi/no \n").lower()
        if confirmacion == "no":
            print("has cancelado la curacion")
        elif confirmacion == "si":
            pokemon_curar.curar()
            self.dinero -= 100
            print(f"has curado a {pokemon_curar.nombre}, te queda {self.dinero} de oro")

        else:
            print("opcion no valida, se cancela la curacion")
    
    def menu_curacion(self):
        curacion = input("quieres curar a tus pokemons: si/no\n").lower()
        if curacion == "no":
            print("no has querido curar a tu pokemon")
        while curacion == "si":
            self.ver_equipo()
            opcion = input("elige el slot para curar al pokemon: ").lower()
            if opcion not in self.pokemons or self.pokemons[opcion] is None:
                print("no se ha podido curar el pokemon por que el slot esta vacio o el pokemon tiene full HP")
            elif opcion in self.pokemons:
                slot_pokemones = self.pokemons[opcion]
                if slot_pokemones is not None:
                    index = self.evo_index[opcion]
                    pokemon_curar = slot_pokemones[index]
                    self.regenerar(pokemon_curar)
            else:
                print("opcion no valida")
            curacion = input("quieres curar a otro pokemon? \nsi/no\n").lower()
            if curacion == "no":
                print("has salido del menú de curación")
                False

    
                
    def todos_ko(self):
        for slot, linea in self.pokemons.items():
            if linea is not None:
                index = self.evo_index[slot]
                if linea[index].hp_actual > 0:
                    return False  
        return True  
    
    def cambiar_pokemon(self):
        cambio = True
        while cambio:
            if self.todos_ko == True:
                cambio = False
                return False
            else:
                self.ver_equipo()
                opcion = input("a que slot quieres cambiar: ").lower()
                if opcion not in self.pokemons:
                    print("Slot no válido")
                elif self.pokemons[opcion] is None:
                    print("Ese slot está vacío")
                else:
                    index = self.evo_index[opcion]
                    pokemon = self.pokemons[opcion][index]
                    if pokemon.hp_actual <= 0:
                        print("Ese pokemon está fuera de combate")
                    else:
                        cambio = False
                        return opcion, pokemon



#pokemons
bulbasaur = Tipo("bulbasaur", "planta", 200, 10)
ivysaur = Tipo("ivysaur", "planta", 350, 20)
venusaur = Tipo("venusaur", "planta", 450, 30)
charmander = Tipo("charmander", "fuego", 100, 30)
charmeleon = Tipo("charmeleon", "fuego", 200, 40)
charizard = Tipo("charizard", "fuego", 300, 50)
squirtle = Tipo("squirtle", "agua", 200, 20)
wartortle = Tipo("wartortle", "agua", 300, 30)
blastoise = Tipo("blastoise", "agua", 400, 40)
caterpie = Tipo("caterpie", "bicho", 75, 10)
metapod = Tipo("metapod", "bicho", 200, 15)
butterfree = Tipo("butterfree", "bicho", 300, 30)
weedle = Tipo("weedle", "bicho", 75, 10)
kakuna = Tipo("kakuna", "bicho", 150, 20)
beedrill = Tipo("beedrill", "bicho", 200, 35)
pidgey = Tipo("pidgey", "volador", 100, 10)
pidgeotto = Tipo("pidgeotto", "volador", 150, 25)
pidgeot = Tipo("pidgeot", "volador", 250, 45)
rattata = Tipo("rattata", "normal", 100, 5)
raticate = Tipo("raticate", "normal", 200, 10)
spearow = Tipo("spearow", "volador", 100, 10)
fearow = Tipo("fearow", "volador", 200, 20)
ekans = Tipo("ekans", "veneno", 100, 5)
arbok = Tipo("arbok", "veneno", 200, 15)
pikachu = Tipo("pikachu", "electrico", 200, 20)
raichu = Tipo("raichu", "electrico", 300, 30)
sandshrew = Tipo("sandshrew", "tierra", 150, 10)
sandslash = Tipo("sandslash", "tierra", 300, 25)
nidoranH = Tipo("nidoranf", "veneno", 75, 5)
nidorina = Tipo("nidorina", "veneno", 125, 15)
nidoqueen = Tipo("nidoqueen", "veneno", 200, 30)
nidoranM = Tipo("nidoranm", "veneno", 75, 5)
nidorino = Tipo("nidorino", "veneno", 125, 15)
nidoking = Tipo("nidoking", "veneno", 200, 30)
clefairy = Tipo("clefairy", "normal", 200, 5)
clefable = Tipo("clefable", "normal", 400, 10)
vulpix = Tipo("vulpix", "fuego", 100, 10)
ninetales = Tipo("ninetales", "fuego", 250, 30)
jigglypuff = Tipo("jigglypuff", "normal", 150, 10)
wigglytuff = Tipo("wigglytuff", "normal", 300, 20)
zubat = Tipo("zubat", "veneno", 100, 10)
golbat = Tipo("golbat", "veneno", 200, 20)
oddish = Tipo("oddish", "planta", 75, 10)
gloom = Tipo("gloom", "planta", 125, 20)
vileplume = Tipo("vileplume", "planta", 225, 35)
paras = Tipo("paras", "bicho", 100, 5)
parasect = Tipo("parasect", "bicho", 200, 25)
venonat = Tipo("venonat", "bicho", 100, 10)
venomoth = Tipo("venomoth", "bicho", 250, 25)
diglett = Tipo("diglett", "tierra", 150, 10)
dugtrio = Tipo("dugtrio", "tierra", 250, 20)
meowth = Tipo("meowth", "normal", 100, 15)
persian = Tipo("persian", "normal", 200, 25)
psyduck = Tipo("psyduck", "agua", 100, 10)
golduck = Tipo("golduck", "agua", 200, 25)
mankey = Tipo("mankey", "lucha", 100, 15)
primeape = Tipo("primeape", "lucha", 200, 35)
growlithe = Tipo("growlithe", "fuego", 100, 15)
arcanine = Tipo("arcanine", "fuego", 200, 25)
poliwag = Tipo("poliwag", "agua", 100, 10)
poliwhirl = Tipo("poliwhirl", "agua", 200, 20)
poliwrath = Tipo("poliwrath", "agua", 300, 30)
abra = Tipo("abra", "psiquico", 75, 15)
kadabra = Tipo("kadabra", "psiquico", 125, 30)
alakazam = Tipo("alakazam", "psiquico", 200, 45)
machop = Tipo("machop", "lucha", 100, 10)
machoke = Tipo("machoke", "lucha", 200, 20)
machamp = Tipo("machamp", "lucha", 300, 35)
bellsprout = Tipo("bellsprout", "planta", 100, 10)
weepinbell = Tipo("weepinbell", "planta", 200, 20)
victreebel = Tipo("victreebel", "planta", 300, 30)
tentacool = Tipo("tentacool", "agua", 150, 10)
tentacruel = Tipo("tentacruel", "agua", 250, 25)
geodude = Tipo("geodude", "roca", 150, 10)
graveler = Tipo("graveler", "roca", 250, 20)
golem = Tipo("golem", "roca", 350, 30)
ponyta = Tipo("ponyta", "fuego", 100, 15)
rapidash = Tipo("rapidash", "fuego", 200, 25)
slowpoke = Tipo("slowpoke", "agua", 150, 10)
slowbro = Tipo("slowbro", "agua", 300, 20)
magnemite = Tipo("magnemite", "electrico", 100, 10)
magneton = Tipo("magneton", "electrico", 200, 20)
farfetchd = Tipo("farfetchd", "normal", 150, 20)
doduo = Tipo("doduo", "volador", 100, 10)
dodrio = Tipo("dodrio", "normal", 200, 25)
seel = Tipo("seel", "agua", 100, 10)
dewgong = Tipo("dewgong", "agua", 200, 20)
grimer = Tipo("grimer", "veneno", 100, 10)
muk = Tipo("muk", "veneno", 200, 20)
shellder = Tipo("shellder", "agua", 150, 10)
cloyster = Tipo("cloyster", "agua", 300, 20)
gastly = Tipo("gastly", "fantasma", 75, 10)
haunter = Tipo("haunter", "fantasma", 125, 20)
gengar = Tipo("gengar", "fantasma", 200, 35)
onix = Tipo("onix", "roca", 200, 10)
drowzee = Tipo("drowzee", "psiquico", 75, 15)
hypno = Tipo("hypno", "psiquico", 125, 30)
krabby = Tipo("krabby", "agua", 100, 10)
kingler = Tipo("kingler", "agua", 200, 20)
voltorb = Tipo("voltorb", "electrico", 100, 10)
electrode = Tipo("electrode", "electrico", 200, 20)
exeggcute = Tipo("exeggcute", "planta", 100, 10)
exeggutor = Tipo("exeggutor", "planta", 200, 20)
cubone = Tipo("cubone", "tierra", 100, 10)
marowak = Tipo("marowak", "tierra", 250, 25)
hitmonlee = Tipo("hitmonlee", "lucha", 150, 25)
hitmonchan = Tipo("hitmonchan", "lucha", 150, 25)
lickitung = Tipo("lickitung", "normal", 200, 10)
koffing = Tipo("koffing", "veneno", 100, 10)
weezing = Tipo("weezing", "veneno", 200, 20)
rhyhorn = Tipo("rhyhorn", "tierra", 150, 10)
rhydon = Tipo("rhydon", "tierra", 250, 20)
chansey = Tipo("chansey", "normal", 500, 5)
tangela = Tipo("tangela", "planta", 100, 5)
kangaskhan = Tipo("kangaskhan", "normal", 200, 20)
horsea = Tipo("horsea", "agua", 100, 10)
seadra = Tipo("seadra", "agua", 200, 20)
goldeen = Tipo("goldeen", "agua", 100, 10)
seaking = Tipo("seaking", "agua", 200, 20)
staryu = Tipo("staryu", "agua", 150, 10)
starmie = Tipo("starmie", "agua", 250, 25)
mrmime = Tipo("mrmime", "psiquico", 200, 20)
scyther = Tipo("scyther", "bicho", 150, 25)
jynx = Tipo("jynx", "psiquico", 200, 20)
electabuzz = Tipo("electabuzz", "electrico", 150, 15)
magmar = Tipo("magmar", "fuego", 150, 15)
pinsir = Tipo("pinsir", "bicho", 150, 15)
tauros = Tipo("tauros", "normal", 150, 15)
magikarp = Tipo("magikarp", "agua", 50, 5)
gyarados = Tipo("gyarados", "agua", 300, 30)
lapras = Tipo("lapras", "agua", 200, 25)
ditto = Tipo("ditto", "normal", 50, 5)
eevee = Tipo("eevee", "normal", 50, 5)
vaporeon = Tipo("vaporeon", "agua", 200, 20)
jolteon = Tipo("jolteon", "electrico", 200, 20)
flareon = Tipo("flareon", "fuego", 200, 20)
porygon = Tipo("porygon", "normal", 150, 15)
omanyte = Tipo("omanyte", "agua", 100, 10)
omastar = Tipo("omastar", "roca", 200, 20)
kabuto = Tipo("kabuto", "roca", 100, 10)
kabutops = Tipo("kabutops", "roca", 200, 20)
aerodactyl = Tipo("aerodactyl", "roca", 200, 20)
snorlax = Tipo("snorlax", "normal", 400, 10)
articuno = Tipo("articuno", "hielo", 300, 20)
zapdos = Tipo("zapdos", "electrico", 300, 20)
moltres = Tipo("moltres", "fuego", 300, 20)
dratini = Tipo("dratini", "dragon", 100, 10)
dragonair = Tipo("dragonair", "dragon", 200, 25)
dragonite = Tipo("dragonite", "dragon", 300, 40)
mewtwo = Boss("mewtwo", "psiquico", 500, 50)
mew = Boss("mew", "psiquico", 500, 40)

posibles_bosses = [mew, mewtwo, zapdos, moltres, articuno]


#lineas evolutivas
linea_bulbasaur = [bulbasaur, ivysaur, venusaur]
linea_charmander = [charmander, charmeleon, charizard]
linea_squirtle = [squirtle, wartortle, blastoise]
linea_caterpie = [caterpie, metapod, butterfree]
linea_weedle = [weedle, kakuna, beedrill]
linea_pidgey = [pidgey, pidgeotto, pidgeot]
linea_rattata = [rattata, raticate]
linea_spearow = [spearow, fearow]
linea_ekans = [ekans, arbok]
linea_pikachu = [pikachu, raichu]
linea_sandshrew = [sandshrew, sandslash]
linea_nidoran_f = [nidoranH, nidorina, nidoqueen]
linea_nidoran_m = [nidoranM, nidorino, nidoking]
linea_clefairy = [clefairy, clefable]
linea_vulpix = [vulpix, ninetales]
linea_jigglypuff = [jigglypuff, wigglytuff]
linea_zubat = [zubat, golbat]
linea_oddish = [oddish, gloom, vileplume]
linea_paras = [paras, parasect]
linea_venonat = [venonat, venomoth]
linea_diglett = [diglett, dugtrio]
linea_meowth = [meowth, persian]
linea_psyduck = [psyduck, golduck]
linea_mankey = [mankey, primeape]
linea_growlithe = [growlithe, arcanine]
linea_poliwag = [poliwag, poliwhirl, poliwrath]
linea_abra = [abra, kadabra, alakazam]
linea_machop = [machop, machoke, machamp]
linea_bellsprout = [bellsprout, weepinbell, victreebel]
linea_tentacool = [tentacool, tentacruel]
linea_geodude = [geodude, graveler, golem]
linea_ponyta = [ponyta, rapidash]
linea_slowpoke = [slowpoke, slowbro]
linea_magnemite = [magnemite, magneton]
linea_farfetchd = [farfetchd]
linea_doduo = [doduo, dodrio]
linea_seel = [seel, dewgong]
linea_grimer = [grimer, muk]
linea_shellder = [shellder, cloyster]
linea_gastly = [gastly, haunter, gengar]
linea_onix = [onix]
linea_drowzee = [drowzee, hypno]
linea_krabby = [krabby, kingler]
linea_voltorb = [voltorb, electrode]
linea_exeggcute = [exeggcute, exeggutor]
linea_cubone = [cubone, marowak]
linea_hitmonlee = [hitmonlee]
linea_hitmonchan = [hitmonchan]
linea_lickitung = [lickitung]
linea_koffing = [koffing, weezing]
linea_rhyhorn = [rhyhorn, rhydon]
linea_chansey = [chansey]
linea_tangela = [tangela]
linea_kangaskhan = [kangaskhan]
linea_horsea = [horsea, seadra]
linea_goldeen = [goldeen, seaking]
linea_staryu = [staryu, starmie]
linea_mrmime = [mrmime]
linea_scyther = [scyther]
linea_jynx = [jynx]
linea_electabuzz = [electabuzz]
linea_magmar = [magmar]
linea_pinsir = [pinsir]
linea_tauros = [tauros]
linea_magikarp = [magikarp, gyarados]
linea_lapras = [lapras]
linea_ditto = [ditto]
linea_eevee = [eevee, vaporeon, jolteon, flareon]
linea_porygon = [porygon]
linea_omanyte = [omanyte, omastar]
linea_kabuto = [kabuto, kabutops]
linea_aerodactyl = [aerodactyl]
linea_snorlax = [snorlax]
linea_dratini = [dratini, dragonair, dragonite]

#posibles enemigos
posibles_pokemons = [
    linea_bulbasaur,
    linea_charmander ,
    linea_squirtle,
    linea_caterpie ,
    linea_weedle ,
    linea_pidgey ,
    linea_rattata ,
    linea_spearow ,
    linea_ekans ,
    linea_pikachu ,
    linea_sandshrew,
    linea_nidoran_f ,
    linea_nidoran_m ,
    linea_clefairy ,
    linea_vulpix,
    linea_jigglypuff ,
    linea_zubat ,
    linea_oddish ,
    linea_paras ,
    linea_venonat ,
    linea_diglett ,
    linea_meowth ,
    linea_psyduck ,
    linea_mankey ,
    linea_growlithe ,
    linea_poliwag ,
    linea_abra ,
    linea_machop ,
    linea_bellsprout ,
    linea_tentacool ,
    linea_geodude,
    linea_ponyta ,
    linea_slowpoke ,
    linea_magnemite ,
    linea_farfetchd ,
    linea_doduo ,
    linea_seel ,
    linea_grimer,
    linea_shellder ,
    linea_gastly ,
    linea_onix,
    linea_drowzee ,
    linea_krabby ,
    linea_voltorb ,
    linea_exeggcute ,
    linea_cubone ,
    linea_hitmonlee ,
    linea_hitmonchan ,
    linea_lickitung,
    linea_koffing ,
    linea_rhyhorn ,
    linea_chansey ,
    linea_tangela ,
    linea_kangaskhan ,
    linea_horsea ,
    linea_goldeen ,
    linea_staryu ,
    linea_mrmime ,
    linea_scyther,
    linea_jynx ,
    linea_electabuzz,
    linea_magmar ,
    linea_pinsir ,
    linea_tauros,
    linea_magikarp ,
    linea_lapras,
    linea_ditto,
    linea_eevee ,
    linea_porygon ,
    linea_omanyte ,
    linea_kabuto ,
    linea_aerodactyl,
    linea_snorlax ,
    linea_dratini,
]
