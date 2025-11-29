def menu_curacion(self):
        curacion = input("quieres curar a tus pokemons: si/no\n").lower()

        if curacion == "no":
            print("no has querido curar a tu pokemon")
            return

        while curacion == "si":
            self.ver_equipo()
            opcion = input("elige el slot para curar al pokemon: ")

            #se puede escribir "slot x" o el numero del slot
            try:
                numero = int(opcion)
                index = f"slot {numero}"
            except:
                index = opcion.lower()
            
            #slot x no esta en mi equipo
            if index not in self.pokemons:
                print("no se ha podido curar el pokemon por que el slot esta vacio o no existe el slot")
            #pokemon tiene full hp
            elif self.pokemons[index].hp == self.pokemons[index].hp_actual:
                print("Ese pokemon tiene full HP")
            #slot esta en mi equipo
            elif index in self.pokemons:
                slot_pokemones = self.pokemons[index] 
                index = self.evo_index[index]
                pokemon_curar = slot_pokemones[index]
                self.regenerar(pokemon_curar)

            else:
                print("opcion no valida")
            curacion = input("quieres curar a otro pokemon? \nsi/no\n").lower()

            if curacion == "no":
                print("has salido del menú de curación")