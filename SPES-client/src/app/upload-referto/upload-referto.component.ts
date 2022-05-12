import { Component, OnInit } from '@angular/core';
import {HttpClient} from "@angular/common/http";
import {Router} from "@angular/router";
import {WalletService} from "../../api/wallet.service";
import {ToastrService} from "ngx-toastr";
import {FormBuilder, Validators} from "@angular/forms";
import {DatePipe} from "@angular/common";
import {ReportService} from "../../api/report.service";

@Component({
  selector: 'app-upload-referto',
  templateUrl: './upload-referto.component.html',
  styleUrls: ['./upload-referto.component.css']
})
export class UploadRefertoComponent implements OnInit {
  public responsePdf: any;
  public pdfChosen = false


  constructor(private http: HttpClient, private router: Router, public service: ReportService, private toastr: ToastrService, private fb: FormBuilder, private datepipe: DatePipe) {
  }

  format: string = 'yyyy-MM-dd';
  formModel = this.fb.group({
    Titolo: ['', Validators.required],


  });

  ngOnInit() {
    this.formModel.reset();
  }

  onSubmit() {
    var exp_date = String(this.datepipe.transform(this.formModel.value.Expiration_Date, this.format));
    console.log(exp_date)
    var releaseDate = String(this.datepipe.transform(this.formModel.value.Release_Date, this.format));
    console.log(releaseDate)
    let idPf = String(localStorage.getItem("idPf"))
    this.service.uploadMedicalReportReportsUploadPost(this.responsePdf,idPf, this.formModel.value.Titolo, "body", true ).subscribe(
      {
        next: value => {
          console.log(value)
          this.formModel.reset();
          this.toastr.success('Effettuato l\'upload del referto!', 'L\'inserimento ha avuto successo!');
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

  onLogout() {
    localStorage.removeItem('token');
    this.router.navigate(['login'])
  }


  public uploadFinished = (event: any) => {
    this.responsePdf = event;
    this.pdfChosen = true
  }
}
