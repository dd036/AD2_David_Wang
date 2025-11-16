import random
import pokemons as pok

num_partida = 0
partida = input("Quieres empezar la partida? \nsi/no \n").lower()
tutorial = True
eleccion = True
player = pok.Equipo() 
slot = "slot 1"

while partida == "si":
    Gary = pok.bulbasaur
    nivel_oponente = random.randint(1,3)
    x = random.randint(0,len(pok.posibles_pokemons)-1)
    lin_oponente = pok.posibles_pokemons[x]      # línea evolutiva
    oponente = lin_oponente[0]  
    oponente.nivel = nivel_oponente
    oponente.cambio_stats(nivel_oponente)
    oponente.curar()
    turno = 1

    #eleccion de inicial
    while eleccion == True:
        inicial =input("puedes elegir uno de los 3 pokemon: " 
        "charmander, " 
        "squirtle, " 
        "bulbasaur: ").lower()

        if inicial == "charmander":
            player.pokemons["slot 1"] = pok.linea_charmander
            eleccion = False

        elif inicial == "squirtle":
            player.pokemons["slot 1"] = pok.linea_squirtle
            eleccion = False

        elif inicial == "bulbasaur":
            player.pokemons["slot 1"] = pok.linea_bulbasaur
            eleccion = False

        else:
            print("eres dislexico y no sabes escribir")

    print(f"perfecto, has elegido a {inicial} como tu inicial, ahora vas a tener tu primera batalla, y te vas a enfrentar a Gary \nhas elegido a {inicial}, Gary a sacado bulbasur\n")

        
    pokemon_activo = player.pokemons[slot][player.evo_index[slot]]

    #tutorial vs Gary
    while tutorial == True:
        while pokemon_activo.hp_actual > 0 and Gary.hp_actual > 0:
            print(f"{5*'-'} Turno {turno} {5*'-'}")
            accion = int(input("Escribe 1 para atacar: "))

            if accion == 1:
                daño = round(pokemon_activo.atacar(Gary), 2)
                print(f"Has atacado a Bulbasur y le has hecho {daño} de daño. Le queda {round(Gary.hp_actual,2)}/{Gary.hp}HP")

            if Gary.hp_actual > 0:
                daño = round(Gary.atacar(pokemon_activo), 2)
                print(f"Bulbasur te ha atacado y te ha hecho {daño} de daño. Te queda {round(pokemon_activo.hp_actual,2)}/{pokemon_activo.hp} HP \n")

            turno += 1

        print("fin del combate")
        if pokemon_activo.hp_actual <= 0 and Gary.hp_actual > 0:
            print("has perdido la partida")
        elif pokemon_activo.hp_actual > 0 and Gary.hp_actual <= 0:
            dinero_ganado = random.randint(200, 300)
            print(f"has ganado la partida, has ganado {dinero_ganado} de oro")
            pokemon_activo.nivel += 1
            pokemon_activo.cambio_stats(1)
            print(f"{pokemon_activo.nombre} ha subido de nivel, sus nuevos stats son:\n"
              f"{pokemon_activo.ataque} ataque\n"
              f"{pokemon_activo.hp} max HP")
            player.dinero += dinero_ganado
            print(f"tu pokemon a subido de nivel, ahora es nivel {pokemon_activo.nivel}")
        else:
            print("ha sido un empate")
        print(f"enorabuena!!! has terminado el tutorial, ahora vamos a empezar una nueva batalla \n")
        tutorial = False
        pokemon_activo.curar()  
    

    #siguiente partida
    num_partida += 1
    turno = 1
    capturado = 1

    print(f"{5*'-'} partida {num_partida} {5*'-'}")
    print(f"tu oponente es {oponente.nombre}\n"
          f"nivel {oponente.nivel}\n"
          f"{oponente.hp_actual}/{oponente.hp}HP\n"
          f"{oponente.ataque} ataque")

    while (pokemon_activo.hp_actual > 0 and oponente.hp_actual > 0) and capturado == 1:
        print(f"{5*'-'} turno {turno} {5*'-'}")
        accion = int(input("1=ATACAR / 2=CAPTURAR / 3=CAMBIAR DE POKEMON: "))

        if accion == 1:
            daño = round(pokemon_activo.atacar(oponente), 2)
            print(f"{pokemon_activo.nombre} ha atacado a {oponente.nombre} y le has hechp {daño} de daño. Le queda {round(oponente.hp_actual,2)}/{oponente.hp} HP")

        elif accion == 2:
            posibilidad = oponente.posible_captura()
            probabilidad = random.random()
            if posibilidad < probabilidad:
                print(f"has fallado en capturar a {oponente.nombre}, pierdes el turno")
                capturado = 1
            else:
                no_capturado = player.agregar_pokemon(lin_oponente)
                if no_capturado:
                    capturado = 1
                else:
                    capturado = 0
                    print(f"enhorabuena, has capturado a {oponente.nombre}")
    
        elif accion == 3:
            slot, pokemon_activo = player.cambiar_pokemon()
        
        else:
            print("eso no es posible, pierdes el turno")

        if oponente.hp_actual > 0 and capturado == 1:
            daño = round(oponente.atacar(pokemon_activo), 2)
            print(f"{oponente.nombre} te ha atacado y te ha hecho {daño} de daño. A {pokemon_activo.nombre} le queda {round(pokemon_activo.hp_actual,2)}/{pokemon_activo.hp} HP \n")
        
        if pokemon_activo.hp_actual <= 0:
            print(f"{oponente.nombre} ha derrotado a {pokemon_activo.nombre}")
            if player.todos_ko() == True:
                print("todos tus pokemons estan fuera de combate")
            else:
                resultado = player.cambiar_pokemon()
                if resultado is not None:
                    slot, pokemon_activo = resultado
                

        turno += 1
    
    print("fin del combate")
    if capturado == 0:
        print(f"has capturado a {oponente.nombre}, ahora es parte de tu equipo \n")

    else:
        if pokemon_activo.hp_actual <= 0 and oponente.hp_actual > 0:
            print("has perdido la partida")
            partida = input("quieres volver a empezar? \nsi/no \n")
            if partida == "si":
                tutorial = True
                eleccion = True
                num_partida = 1

        elif pokemon_activo.hp_actual > 0 and oponente.hp_actual <= 0:
            pokemon_activo.nivel += 1
            oro = random.randint(200,300)
            player.dinero += oro
            print(f"has ganado la partida, has ganado {oro} de oro, ahora tienes {player.dinero} de oro en total")
            print(f"tu {pokemon_activo.nombre} a subido de nivel, ahora es nivel {pokemon_activo.nivel}")
            pokemon_activo.cambio_stats(1)
            print(f"{pokemon_activo.nombre} ha subido de nivel, sus nuevos stats son:\n"
              f"{pokemon_activo.ataque} ataque\n"
              f"{pokemon_activo.hp} max HP")
        else:
            print("ha sido un empate")
    if partida == "si":
        #boss fight
        #num_partida = 5
        if num_partida % 5 == 0:
            transformacion = True
            player.menu_curacion()
            turno = 1
            enemigo_boss = pok.posibles_bosses [random.randint(1, len(pok.posibles_bosses)-1)]
            print(f"es hora de tu primer boss fight, te vas a enfrentar a {enemigo_boss.nombre} \n{enemigo_boss.nombre}: {enemigo_boss.hp_actual}/{enemigo_boss.hp}hp \nataque: {enemigo_boss.ataque}")

            while enemigo_boss.hp_actual > 0 and pokemon_activo.hp_actual > 0:
                print(f"{5*'-'} TURNO {turno} {5*'-'}")
                accion = int(input("1=ATACAR / 2=CAPTURAR / 3=CAMVIAR DE POKEMON: "))

                if accion == 1:
                    daño = round(pokemon_activo.atacar(enemigo_boss), 2)
                    print(f"{pokemon_activo.nombre} ha atacado a {enemigo_boss.nombre}, le ha hecho {daño} de daño. Le queda {round(enemigo_boss.hp_actual,2)}/{enemigo_boss.hp} HP")

                elif accion == 2:
                    print("no puedes capturar a un boss, pierdes el turno")
                
                elif accion == 3:
                    slot, pokemon_activo = player.cambiar_pokemon()
                
                else:
                    print("eso no es posible, pierdes el turno")

                if enemigo_boss.hp_actual <= enemigo_boss.hp/2 and transformacion == True:
                    enemigo_boss.final_form()
                    print(f"el boss final ha usado su forma final:")
                    print(f"boss final: hp = {enemigo_boss.hp_actual}, ataque = {enemigo_boss.ataque}")
                    transformacion = False

                if enemigo_boss.hp_actual > 0:
                    daño = round(enemigo_boss.atacar(pokemon_activo), 2)
                    print(f"{enemigo_boss.nombre} te ha atacado y ha hecho {daño} de daño, te queda {pokemon_activo.hp_actual}/{pokemon_activo.hp} HP\n")
                
                if pokemon_activo.hp_actual <= 0:
                    print(f"{enemigo_boss.nombre} ha derrotado a {pokemon_activo.nombre}")
                    if player.todos_ko() == True:
                        print("todos tus pokemons estan fuera de combate")
                        print("has perdido la partida")
                        partida = input("quieres seguir jugando? si/no\n")
                    else:
                        slot, pokemon_activo = player.cambiar_pokemon()
                
                turno += 1
                
            
            if enemigo_boss.hp_actual < 0 and pokemon_activo.hp_actual > 0:
                oro = random.randint(500, 700)
                print(f"enhorabueana, ha derrotado a un boss, tu pokemon a subido 5 nivels y has ganado {oro} de oro")
                player.dinero += oro
                pokemon_activo.nivel += 5
                pokemon_activo.cambio_stats(5)
                print(f"{pokemon_activo.nombre} ha subido de nivel, sus nuevos stats son:\n"
                f"{pokemon_activo.ataque} ataque\n"
                f"{pokemon_activo.hp} max HP")
            elif enemigo_boss.hp_actual > 0 and player.todos_ko():
                print("has perdido el boss fight")
            else:
                print("ha sido un empate")
        
    #evolucion
    num_evo = len(player.pokemons[slot])
    index_actual = player.evo_index[slot]
    nuevo_index = index_actual
    
    if num_evo == 3:
        if 3 >= pokemon_activo.nivel >= 0:
            nuevo_index = 0
        elif 10 >= pokemon_activo.nivel > 3:
            nuevo_index = 1
        else:
            nuevo_index = 2
    elif num_evo == 2:
        if 5 >= pokemon_activo.nivel >= 0:
            nuevo_index = 0
        else:
            nuevo_index = 1
    
    if nuevo_index != index_actual:
        player.evo_index[slot] = nuevo_index      
        pokemon_activo = player.pokemons[slot][nuevo_index]
        pokemon_activo.curar()
        print(f"enhorabuena, tu pokemon a evolucionado y ahora es un {pokemon_activo.nombre} \n"
            f"{pokemon_activo.nombre}:\n"
            f"{pokemon_activo.hp_actual}/{pokemon_activo.hp} HP\n"
            f"ataque = {pokemon_activo.ataque}"
            )

    if partida == "si":
        #mostrar equipo
        if player.todos_ko() == False:
            mostrar_equipo = input("quieres ver tu equipo? si/no\n").lower()
            if mostrar_equipo == "si":
                player.ver_equipo()


    partida = input("quieres seguir jugando. \nsi/no \n")
    player.menu_curacion()
