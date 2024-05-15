"""

Este es el modulo que incluye la clase de 
Reproductor de musica
"""

class Player:
    """
    Esta clase crea un reproductor
    de musica
    """

    def play(self, song):
        """
        Reproduce la cancion que recibio 
        como parametro:

        Parameters:
            song(str) : Este es un string con el path 
            o ruta de la cancion a reporducir

        Returns:

            int : Devuelve 1 si el resultado es el 
            correcto y si no retorna 0
        """
        print(f'Reproduciendo la cancion {song}')

    def stop(self):
        print("Stopping")