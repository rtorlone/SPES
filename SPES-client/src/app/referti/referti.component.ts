import {Component, EventEmitter, OnInit, Output} from "@angular/core";
import {HttpClient} from "@angular/common/http";
import {AuthService} from "../../api/auth.service";
import {ToastrService} from "ngx-toastr";
import {Router} from "@angular/router";
import {ReportService} from "../../api/report.service";
import {PfId} from "../../model/pfId";
import {ReportOnlyId} from "../../model/reportOnlyId";
import {waitForAsync} from "@angular/core/testing";

@Component({
  selector: "app-referti",
  templateUrl: "./referti.component.html",
  styleUrls: ["./referti.component.css"],
})
export class RefertiComponent implements OnInit {
  // @ts-ignore
  referti;
  showCarrello = false;
  current = "noFilter";
  isMED = this.userService.roleMatch(["MED"]);
  isPF = this.userService.roleMatch(["PF"]);
  searchText: string = "";
  nome = "Referti";
  page = 1;
  total = 0;
  count = 0;
  limit = 100;
  // @ts-ignore
  totalPages;
  loading = false;
  selectedReportsForPermissions: Array<string> = [];
  @Output() public personaEmitter = new EventEmitter();

  constructor(
    private http: HttpClient,
    private userService: AuthService,
    private toastr: ToastrService,
    private service: ReportService,
    private router: Router
  ) {
  }

  ngOnInit() {
    this.getReferti();
    if(this.isMED){
    this.service.getReportsFromSessionSessionReportsGet().subscribe({
      next: value => {
        this.count = value.length

      }
    })}
  }

  clearFilter() {
    this.searchText = "";
  }

  getReferti(): void {
    if (this.isMED) {
      let id = String(localStorage.getItem("idPf"));

      this.service.getAllMedicalReportsByPfIdReportsPfIdPfGet(id).subscribe({
        next: (value) => {
          this.referti = value;
          this.loading = false;
        },
        error: (err) => {
          this.toastr.error(err.statusText, "Errore nella ricerca!");
        },
        complete: () => console.log(),
      });
    } else if (this.isPF) {
      this.service.getAllMedicalReportsReportsGet().subscribe({
        next: (value) => {
          this.referti = value;
          this.loading = false;
        },
        error: (err) => {
          this.toastr.error(err.statusText, "Errore nella ricerca!");
        },
        complete: () => console.log(),
      });
    }
  }

  pdfOpen(idRef: any) {
    this.service.getMedicalReportByIdReportsIdRefertoGet(idRef).subscribe({
      next: value => {

        let url = window.URL.createObjectURL(value);

        let anchor = document.createElement('a');
        anchor.href = url;

        anchor.target = '_blank';
        anchor.click();
      }
    })
  }

  onClickReferto(idRef: any) {
    localStorage.setItem("idRef", idRef);
  }


  filter() {
    this.getReferti();
  }

  updateSelectedReportsForPermissions(reportId: any) {

    this.selectedReportsForPermissions.push(reportId);
    let array: Array<ReportOnlyId> = [];
    this.selectedReportsForPermissions.forEach((elem) => {
      array.push({report_id: elem});
    });

    this.service.addReportsFromSessionSessionReportsPost(array).subscribe({
      next: (value) => {
        this.toastr.success("Richiesta aggiunta al carrello!", "Success!");
        this.count = value
      },
      error: (err) => {
        this.toastr.error(err.statusText, "Fail!");
      },
      complete: () => {
      },
    });

  }

  show() {
    this.service.getReportsFromSessionSessionReportsGet().subscribe({
      next: value => {
        this.count = value.length

      },
      error:err => {
         this.count = 0
      }
    })
    this.showCarrello = !this.showCarrello;

  }

  goToPrevious(): void {
    this.page--;
    this.getReferti();
  }

  goToNext(): void {
    this.page++;
    this.getReferti();
  }

  goToPage(n: number): void {
    this.page = n;
    this.getReferti();
  }

  public removed = (event: any) => {
    this.count--
  }
    public empty = (event: any) => {
    this.count= 0
  }
}
