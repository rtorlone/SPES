import {Component, EventEmitter, OnInit, Output} from '@angular/core';
import {ReportService} from "../../api/report.service";
import {ToastrService} from "ngx-toastr";
import {ReportId} from "../../model/reportId";

@Component({
  selector: 'app-carrello',
  templateUrl: './carrello.component.html',
  styleUrls: ['./carrello.component.css']
})
export class CarrelloComponent implements OnInit {
  carrello: any = []
  @Output() public remove = new EventEmitter();
  @Output() public empty = new EventEmitter();
  showCarrello = false;

  constructor(private service: ReportService, private toastr: ToastrService) {
  }


  ngOnInit(): void {
    // @ts-ignore
    //this.carrello  = JSON.parse(localStorage.getItem("selectedReportsForPermissions"))
    this.getCarrello()

  }

  onSubmit() {
    this.getCarrello()
    let reportIds: Array<ReportId> = []

    // @ts-ignore
    this.carrello.forEach(item => {
      reportIds.push({report_id: item.report_id})
    })
    this.service.askForMedicalReportsPermissionPermissionsPost(reportIds).subscribe({
      next: value => {
        this.toastr.success("Richieste inviate", "Success!")
      },
      error: err => {
        this.toastr.error(err.statusText, "Fail!")
      },
      complete: () => {
      }
    })
    this.service.emptyReportsFromSessionSessionReportsDelete().subscribe({})
    this.empty.emit()
    this.getCarrello()
  }

  rimuoviRichiesta(idRef: any) {
    this.service.deleteReportFromSessionSessionReportsIdRefertoDelete(idRef).subscribe({
      next: value => {
        this.toastr.success("Richiesta rimossa", "Success!")
      },
      error: err => {
        this.toastr.error(err.statusText, "Fail!")
      },
      complete: () => {
      }
    })
    this.remove.emit()
    this.getCarrello()
  }

  getCarrello() {
    this.service.getReportsFromSessionSessionReportsGet().subscribe({
      next: value => {
        this.carrello = value;
        console.log(value)
      },
      error: err => {
        console.log(err)
        if (err.status == 404) {
          this.carrello = []
        } else {
          this.toastr.error(err.statusText, "Fail!")
        }
      },
      complete: () => {
      }
    })
  }

  show() {
    this.showCarrello = !this.showCarrello;
  }
}
