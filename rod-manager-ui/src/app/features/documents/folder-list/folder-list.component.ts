import {Component, EventEmitter, Input, Output} from '@angular/core';
import {Document, Leaf} from "../document";

import {FormBuilder, FormGroup, Validators} from "@angular/forms";
import {NgxSpinnerService} from "ngx-spinner";
import {ToastrService} from "ngx-toastr";
import {DocumentsService} from "../documents.service";
import {HttpClient, HttpHeaders} from "@angular/common/http";
import {StorageService} from "../../../core/storage/storage.service";
import {Observable} from "rxjs";


@Component({
  selector: 'app-folder-list',
  templateUrl: './folder-list.component.html',
  styleUrls: ['./folder-list.component.scss']
})
export class FolderListComponent {
  @Input() documents!: Document[] | undefined;
  @Input() level!: number
  @Input() parent!: number | null
  @Output() itemAdded: EventEmitter<void> = new EventEmitter<void>();
  addFileForm: FormGroup;
  editFileForm: FormGroup;
  addListForm: FormGroup;
  editListForm: FormGroup;
  showAddDocumentForm = false;
  showEditDocumentForm = false;
  showAddListForm = false;
  showEditListForm = false;
  selectedFile: File | null = null;
  maxFileSize_MB = 200

  constructor(
    formBuilder: FormBuilder,
    private documentsService: DocumentsService,
    private spinner: NgxSpinnerService,
    private toastr: ToastrService,
    private tokenStorageService: StorageService,
    private http: HttpClient
  ) {
    this.addFileForm = formBuilder.group({
      name: ['', [
        Validators.required,
      ]],
      file: ['', [
        Validators.required,
      ]]
    })
    this.editFileForm = formBuilder.group({
      name: ['', [
        Validators.required,
      ]],
      file: ['', []]
    })
    this.editListForm = formBuilder.group({
      name: ['', [
        Validators.required,
      ]],
    })
    this.addListForm = formBuilder.group({
      name: ['', [
        Validators.required,
      ]],
    })
  }

  errorMessages = {
    name: [
      {type: 'required', message: 'Proszę podać nazwę'},
    ],
    file: [
      {type: 'required', message: 'Proszę podać plik'},
    ],
  }

  validationErrors(controlName: string, form: FormGroup): any[] {
    let errors = []
    // @ts-ignore
    for (let error of this.errorMessages[controlName]) {
      if (form.get(controlName)?.hasError(error.type)) {
        errors.push(error);
      }
    }
    return errors;
  }

  // downloadFile(link: string | undefined)
  // {
  //   const fullLink = "/api/adminfile" + link;
  //   window.open(fullLink, '_blank');
  // }


  downloadFile(link: string): void {
    this.downloadFile2(link)
      .subscribe(blob => {
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = this.getFilenameFromPath(link);
        a.click();
        window.URL.revokeObjectURL(url);
      }, error => {
        console.error('Error downloading the file', error);
      });
  }

  getFilenameFromPath(path: string): string {
    const parts = path.split('/');
    return parts[parts.length - 1];
  }

  downloadFile2(link: string): Observable<Blob> {
    const fullLink = "/api/adminfile" + link;
    return this.http.get(fullLink, {responseType: 'blob'});
  }


  addNewDocument(item
                   :
                   Document
  ) {
    if (this.addFileForm.valid && this.selectedFile) {
      const newTitle: string = this.addFileForm.get('name')?.value;
      const newDocument: Leaf = {name: newTitle, file: this.selectedFile, parent: item.id};
      this.spinner.show()
      this.documentsService.postDocuments(newDocument).subscribe({
        next: value => {
          this.updateDocumentsListFromLevel(this.level)
          // this.itemAdded.emit();
          this.showAddDocumentForm = false
        }, error: error => {
          console.error(error);
          this.spinner.hide();
          this.toastr.error('Nie udało się dodać dokumentu', 'Błąd')
        }
      });
    }
  }

  editDocument(item
                 :
                 Document
  ) {
    if (this.editFileForm.valid) {
      const newTitle: string = this.editFileForm.get('name')?.value;
      const id = item.id

      const newLeaf: Leaf = {name: newTitle, file: this.selectedFile, parent: this.parent};
      this.spinner.show()
      this.documentsService.putDocuments(newLeaf, id).subscribe({
        next: value => {
          this.updateDocumentsListFromLevel(this.level)
          this.showEditDocumentForm = false
        }, error: error => {
          console.error(error);
          this.spinner.hide();
          this.toastr.error('Nie udało się edytować dokumentu', 'Błąd')
        }
      })
    }
  }

  addNewList(item
               :
               Document
  ) {
    if (this.addListForm.valid) {
      const newTitle: string = this.addListForm.get('name')?.value;
      const newDocument: Leaf = {name: newTitle, parent: item.id};
      this.spinner.show()
      this.documentsService.postDocuments(newDocument).subscribe({
        next: value => {
          this.updateDocumentsListFromLevel(this.level)
          // this.itemAdded.emit();
          this.showAddListForm = false
        }, error: error => {
          console.error(error);
          this.spinner.hide();
          this.toastr.error('Nie udało się dodać folderu', 'Błąd')
        }
      });
    }
  }

  editList(item
             :
             Document
  ) {
    if (this.editListForm.valid) {
      const newTitle: string = this.editListForm.get('name')?.value;
      const newDocument: Leaf = {name: newTitle, parent: this.parent};
      this.documentsService.putDocuments(newDocument, item.id).subscribe({
        next: value => {
          this.spinner.show()
          this.updateDocumentsListFromLevel(this.level)
          // this.itemAdded.emit();
          this.showAddListForm = false
        },
        error: error => {
          console.error(error);
          this.spinner.hide();
          this.toastr.error('Nie udało się edytować folderu', 'Błąd')
        }
      });
    }
  }

  delete(item
           :
           Document
  ) {
    this.spinner.show()
    this.documentsService.deleteDocument(item.id).subscribe({
      next: value => {
        this.updateDocumentsListFromLevel(this.level)
        // this.itemAdded.emit();
      }, error: error => {
        console.error(error);
        this.spinner.hide();
        this.toastr.error('Nie udało się usunąć', 'Błąd')
      }
    });
  }

  toggleAddDocumentForm() {
    this.showAddDocumentForm = !this.showAddDocumentForm;
    this.addFileForm.reset()
  }

  toggleEditDocumentForm(Document
                           :
                           Document
  ) {
    this.showEditDocumentForm = !this.showEditDocumentForm;
    this.addFileForm.reset()
    this.editFileForm.reset()
    this.editFileForm.patchValue({name: Document.name})
    this.selectedFile = null
  }

  toggleEditFolderForm(Document
                         :
                         Document
  ) {
    this.showEditListForm = !this.showEditListForm;
    this.editListForm.reset()
    this.editListForm.patchValue({name: Document.name})
  }

  toggleAddListForm() {
    this.showAddListForm = !this.showAddListForm;
    this.addListForm.reset()
  }

// onFileSelected(event: any) {
//   this.selectedFile = event.target.files[0];
// }

  onFileSelected(event
                   :
                   Event
  ) {
    const fileInput = event.target as HTMLInputElement;
    const selectedFile = fileInput.files?.[0];

    if (selectedFile) {
      if (selectedFile.size > this.maxFileSize_MB * 1024 * 1024) { // Limit 50MB w bajtach
        // Twój kod obsługi błędu, np. wyświetlenie komunikatu o błędzie
        console.log(`Plik jest zbyt duży. Wybierz plik mniejszy niż ${this.maxFileSize_MB}MB.`);
        fileInput.value = ''; // Wyczyszczenie pola wyboru pliku
        this.selectedFile = null;
        this.toastr.error(`Plik jest zbyt duży. Wybierz plik mniejszy niż ${this.maxFileSize_MB}MB.`, 'Błąd')
      } else {
        this.selectedFile = selectedFile
      }
    }
  }

  onItemAdded() {
    this.itemAdded.emit();
  }

  updateDocumentsListFromLevel(level
                                 :
                                 number
  ) {
    this.documentsService.getDocuments()
      .subscribe({
        next: (result: Document[]) => {
          // Aktualizacja listy od określonego poziomu
          this.documents = this.filterDocumentsByLevel(result, level);
          this.spinner.hide();
        }, error: error => {
          console.error(error);
          this.spinner.hide();
          this.toastr.error('Nie udało się pobrać dokumentów', 'Błąd')
        }
      });
  }

  filterDocumentsByLevel(documents
                           :
                           Document[], level
                           :
                           number
  ):
    Document[] {
    if (level <= 1) {
      return documents;
    }

    let filteredDocuments: Document[] = [];

    for (const doc of documents) {
      if (doc.items && doc.items.length > 0) {
        // Rekurencyjnie filtruj dokumenty od następnego poziomu
        const filteredChildren = this.filterDocumentsByLevel(doc.items, level - 1);
        filteredDocuments = filteredDocuments.concat(filteredChildren);
      }
    }

    return filteredDocuments;
  }
}

