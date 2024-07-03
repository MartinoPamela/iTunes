import warnings

import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def handleCreaGrafo(self, e):

        try:
            totDint = int(self._view._txtInDurata.value)
        except ValueError:
            # se entro qua vuol dire che quello che ho aggiunto nel txtfield è una stringa oppure è vuota
            warnings.warn_explicit(message="duration not integer", category=TypeError,
                                   filename="controller.py", lineno=16)
            return

        self._model.buildGraph(totDint)

        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(ft.Text(f"Grafo correttamente creato."))
        nN, nE = self._model.getGraphSize()  # numero nodi e numero archi
        self._view.txt_result.controls.append(ft.Text(f"Il grafo ha {nN} nodi e "
                                                      f"{nE} archi."))

        nodes = self._model.getNodes()  # questi nodi li voglio mettere nel dd
        nodes.sort(key=lambda x: x.Title)  # li sorto in ordine alfabetico per titolo

        # Modo 1 per riempire il dd
        # for n in nodes:
        #     self._view._ddAlbum.options.append(ft.dropdown.Option(
        #                                                         data=n,  # data è l'oggetto
        #                                                         text=n.Title,  # n è un ogg album,lo chiamo col titolo
        #                                                         on_click=self.getSelectedAlbum))

        # Modo 2 con la funzione map
        listDD = map(lambda x: ft.dropdown.Option(data=x, text=x.Title, on_click=self.getSelectedAlbum), nodes)
        # map di un metodo e una lista

        self._view._ddAlbum.options = listDD

        print("done")
        self._view.update_page()

    def getSelectedAlbum(self, e):  # metodo chiamato quando seleziono un elemento dal dd
        print("getSelectedAlbum")
        if e.control.data is None:
            self._choiceAlbum = None
        else:
            self._choiceAlbum = e.control.data
        print(self._choiceAlbum)

    def handleAnalisiComp(self, e):
        if self._choiceAlbum is None:
            warnings.warn("Album field not selected")
            return

        sizeC, totDurata = self._model.getConnessaDetails(self._choiceAlbum)

        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(ft.Text(f"La componente connessa che include {self._choiceAlbum} "
                                                      f"ha dimensione {sizeC} e durata totale {totDurata}"))

        self._view.update_page()

    def handleGetSetAlbum(self, e):

        a1 = self._choiceAlbum
        dTOTtxt = self._view._txtInSoglia.value  # così arriva una stringa, devo assicurarmi che sia un intero

        # controllo input utente

        try:
            dTOT = int(dTOTtxt)
        except ValueError:
            warnings.warn("Soglia not integer")
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text(f"Soglia inserita non valida. Inserire un intero"))
            return

        if self._choiceAlbum is None:
            warnings.warn("Attenzione, album non selezionato. ")
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text(f"Selezionare un album"))
            return

        # se passa try e if allora posso chiamare il metodo del modello

        setAlbum, totD = self._model.getSetAlbum(a1, dTOT)  # mi restituisce un set di album

        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(ft.Text(f"Set di album ottimo trovato con durata totale {totD}."))
        for s in setAlbum:
            self._view.txt_result.controls.append(ft.Text(f"{str(s)}"))

        self._view.update_page()
