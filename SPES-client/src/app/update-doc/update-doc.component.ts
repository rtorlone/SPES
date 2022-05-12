import {Component, OnInit} from '@angular/core';
import {HttpClient} from "@angular/common/http";
import {Router} from "@angular/router";
import {WalletService} from "../../api/wallet.service";
import {ToastrService} from "ngx-toastr";
import {AbstractControl, FormBuilder, ValidationErrors, ValidatorFn, Validators} from "@angular/forms";
import {DatePipe} from "@angular/common";

@Component({
  selector: 'app-update-doc',
  templateUrl: './update-doc.component.html',
  styleUrls: ['./update-doc.component.css']
})
export class UpdateDocComponent implements OnInit {
  public responsePdf: any;
  public responseImg = {dbPath: ''};
  public descrizione = '';
  docToUpdate: any;

  constructor(private http: HttpClient, private router: Router, public service: WalletService, private toastr: ToastrService, private fb: FormBuilder, private datepipe: DatePipe) {
  }

  format: string = 'yyyy-MM-dd';
  formModel = this.fb.group({
    Tipologia: ['', Validators.required],
    Entity: ['', Validators.required],
    Number: ['', Validators.required],
    Place_Of_Issue: ['', Validators.required],
    Release_Date: ['', Validators.required],
    Expiration_Date: ['', Validators.required],

  }, {validator: this.creatDateRangeValidator()});

  creatDateRangeValidator(): ValidatorFn {
    return (form: AbstractControl): ValidationErrors | null => {

      let start: Date = form?.get("Release_Date")?.value

      let end: Date = form?.get("Expiration_Date")?.value;

      if (start && end) {
        start = new Date(start)
        end = new Date(end)
        const isRangeValid = (end.getTime() - start.getTime() > 0);

        return isRangeValid ? null : {dateRange: true};
      }

      return null;
    }
  }

  ngOnInit() {
    this.loadExistingDoc()
  }

  loadExistingDoc() {
    this.docToUpdate = localStorage.getItem("idDoc")
    let idPf = String(localStorage.getItem("idPf"))
    this.service.getIdentificationDocumentByIdWalletPfIdPfDocsDocIdGet(idPf, this.docToUpdate, "response").subscribe({
      next: value => {
        this.formModel.patchValue({
          "Tipologia": value.headers.get("tipologia"),
          "Entity": value.headers.get("entity"),
          "Place_Of_Issue": value.headers.get("place_of_issue"),
          "Number": value.headers.get("number"),
          "Release_Date": value.headers.get("release_date"),
          "Expiration_Date": value.headers.get("expiration_date")
        })


      },
      error: err => {
        this.toastr.error(err.statusText, err.status)

      },
      complete: () => {

      }


    })
  }

  onSubmit() {

    var exp_date = String(this.datepipe.transform(this.formModel.value.Expiration_Date, this.format));

    var releaseDate = String(this.datepipe.transform(this.formModel.value.Release_Date, this.format));


    let idPf = String(localStorage.getItem("idPf"))
    this.service.updateIdentificationDocumentByIdWalletPfIdPfDocsDocIdPut(idPf, this.docToUpdate, this.responsePdf, this.formModel.value.Tipologia, this.formModel.value.Entity, this.formModel.value.Number, this.formModel.value.Place_Of_Issue, releaseDate, exp_date).subscribe(
      {
        next: value => {
          console.log(value)
          this.formModel.reset();
          this.toastr.success('Effettuato l\'upload del documento!', 'L\'inserimento ha avuto successo!');
        },
        error: err => {
          console.log(err);
          console.log(err.statusText);
          this.toastr.error(err.statusText, 'Upload Failed.');
        },
        complete: () => {
        }


      },
    );

  }

  public uploadFinished = (event: any) => {
    this.responsePdf = event;
  }
}
