import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self._choiceGenre = None

    def fillDDGenre(self):
        genres = self._model.getAllGenres()

        for genre in genres:
            self._view._ddGenre.options.append(
                ft.dropdown.Option(data=genre, text=genre.Name, on_click=self._readGenre)
            )
        self._view.update_page()

    def handleCreaGrafo(self, e):
        if self._choiceGenre is None:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(
                ft.Text("Attenzione, seleziona un genere!", color="red")
            )
            self._view.update_page()
            return

        self._model.buildGraph(self._choiceGenre.GenreId)
        num_nodi, num_archi = self._model.getGraphDetails()
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(
            ft.Text("Grafo correttamente creato:", color="green")
        )
        self._view.txt_result.controls.append(
            ft.Text(f"Numero di nodi: {num_nodi}")
        )
        self._view.txt_result.controls.append(
            ft.Text(f"Numero di archi: {num_archi}")
        )
        artist, influenza = self._model.getArtistInfluente()
        self._view.txt_result.controls.append(
            ft.Text(f"Artista più influente: {artist}, con influenza: {influenza}")
        )

        self._view.update_page()

    def handleCreaGrafo(self,e):
        pass

    def handleCammino(self,e):
        pass

    def _readGenre(self, e):
        if e.control.data is None:
            self._choiceGenre = None
        else:
            self._choiceGenre = e.control.data