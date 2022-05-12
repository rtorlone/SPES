import {Component, OnInit, Output, EventEmitter} from '@angular/core';
import {ToastrService} from 'ngx-toastr';
import {WalletService} from "../../api/wallet.service";
import {Router} from '@angular/router';
import {HttpEventType, HttpClient, HttpParameterCodec} from '@angular/common/http';
import {DatePipe} from '@angular/common';
import {AbstractControl, FormBuilder, FormGroup, ValidationErrors, ValidatorFn, Validators} from '@angular/forms';

@Component({
  selector: 'app-upload-form',
  templateUrl: './upload-doc.component.html',
  styles: []
})
export class UploadDocComponent implements OnInit {
  public responsePdf: any;
  public responseImg = {dbPath: ''};
  public descrizione = '';
  public pdfChosen = false
  ;

  constructor(private http: HttpClient, private router: Router, public service: WalletService, private toastr: ToastrService, private fb: FormBuilder, private datepipe: DatePipe) {
  }

  format: string = 'yyyy-MM-dd';
  formModel = this.fb.group({
      Tipologia: ['', Validators.required],
      Entity: ['', Validators.required],
      Number: ['', Validators.required],
      Place_Of_Issue: ['', Validators.required],
      Release_Date: ['', Validators.required],
      Expiration_Date: ['', Validators.required]
    },
    {validator: this.creatDateRangeValidator()});


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
    this.formModel.reset();
  }

  onSubmit() {

    var exp_date = String(this.datepipe.transform(this.formModel.value.Expiration_Date, this.format));
    console.log(exp_date)
    var releaseDate = String(this.datepipe.transform(this.formModel.value.Release_Date, this.format));
    console.log(releaseDate)

    let idPf = String(localStorage.getItem("idPf"))
    this.service.uploadIdentificationDocumentWalletPfIdPfDocsUploadPost(idPf, this.responsePdf, this.formModel.value.Tipologia, this.formModel.value.Entity, this.formModel.value.Number, this.formModel.value.Place_Of_Issue, releaseDate, exp_date).subscribe(
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
    this.pdfChosen = true;
  }
  public uploadImage = (event: any) => {
    this.responseImg = event;
  }
  public parseDescrizione = (event: any) => {
    this.descrizione = event;
    console.log(event);


  }
}
