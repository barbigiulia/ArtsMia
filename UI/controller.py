import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def handleAnalizzaOggetti(self, e):
        self._model.buildGraph()
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(ft.Text("Grafo correttamente creato"))
        self._view.txt_result.controls.append(ft.Text(f"il grafo contiene {self._model.getNumNodes()} "
                                                      f"nodi e {self._model.getNumEdges()} archi"))
        self._view._txtIdOggetto.disabled = False
        self._view._btnCompConnessa.disabled = False
        self._view.update_page() # ricorda sempre di aggiornare la pagina!

    def handleCompConnessa(self,e):

        txtIdOggetto = self._view._txtIdOggetto.value  # recupera il campo dell'utente

        # CONTROLLI DELL'INPUT.......
        if txtIdOggetto.strip()=="":
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text("Attenzione inserire un valore nel campo id", color="red"))
            self._view.update_page()
            return
        try:
            idOggetto = int(txtIdOggetto) # provo a fare la conversione
        except ValueError:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text("Inserire un valore numerico nel campo id", color="red"))
            self._view.update_page()
            return

        #se il num inserito non è presente nel grafico...
        if not self._model.hasNode(idOggetto):
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text("Id inserito non presente nel grafo", color="orange"))
            self._view.update_page()
            return

        # se passa tutti i controlli
        sizeCompConnessa = self._model.getInfoConnessa(idOggetto)
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(ft.Text(f"La componente connessa contenente "
                                                      f"l'oggetto con id {idOggetto} è composta di {sizeCompConnessa} nodi",
                                              color="green"))
        lunValues = range(2,sizeCompConnessa)
        #for v in lunValues:
            #self._view._ddLUN.options.append(ft.dropdown.Option(v))
        lunValuesDD = map(lambda x: ft.dropdown.Option(x), lunValues) # sostituisce il ciclo
        self._view._ddLUN.options= lunValues

        self._view.update_page()




    def handleRicerca(self, e):
        # i controlli li ho già fatti nel meotodo componente connessa
        # e questo bottone posso chiamarlo solo dopo
        source = self._model.getNodeFromId(int(self._view._txtIdOggetto.value))
        lun = self._view._ddLUN.value

        if lun is None:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text("Attenzione selezionare un valore di "
                                                          "lunghezza tra le scelte proposte", color="red"))
            self._view.update_page()
            return
        lunInt = int(lun)  # prima lun è una stringa

        # chiamo il metodo ricorsivo
        path, costo = self._model.getOptPath(source, lun)

        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(ft.Text(f"Ho trovato un cammino che parte da {source} e che ha "
                                                      f"un peso totale pari a {costo}", color="green"))
        self._view.txt_result.controls.append(ft.Text("Di seguito i nodi che compongono questo cammino: ", color="blue"))

        for p in path:
            self._view.txt_result.controls.append(ft.Text(p))

        self._view.update_page()


