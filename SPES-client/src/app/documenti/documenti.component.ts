import {Component, EventEmitter, OnInit, Output} from '@angular/core';
import {HttpClient} from "@angular/common/http";
import {AuthService} from "../../api/auth.service";
import {ToastrService} from "ngx-toastr";
import {ReportService} from "../../api/report.service";
import {Router} from "@angular/router";
import {ReportOnlyId} from "../../model/reportOnlyId";
import {WalletService} from "../../api/wallet.service";

@Component({
  selector: 'app-documenti',
  templateUrl: './documenti.component.html',
  styleUrls: ['./documenti.component.css']
})
export class DocumentiComponent implements OnInit {

 // @ts-ignore
  documenti;
  current = "noFilter";
  isOPS = this.userService.roleMatch(["OPS"]);
  isPF = this.userService.roleMatch(["PF"]);
  searchText: string = "";
  nome = "documenti";
  page = 1;
  total = 0;
  count = 0;
  limit = 100;
  // @ts-ignore
  totalPages;
  loading = false;
  @Output() public personaEmitter = new EventEmitter();

  constructor(
    private http: HttpClient,
    private userService: AuthService,
    private toastr: ToastrService,
    private service: WalletService,
    private router: Router
  ) {}

  ngOnInit() {
    this.getDocs();

  }

  clearFilter() {
    this.searchText = "";
  }

  getDocs(): void {
    let id = ""
    if(this.isOPS){
       id = String(localStorage.getItem("idPf"));}
    else if(this.isPF){
      id = this.userService.getUserId()

    }
    console.log(id)


    this.service.getIdentificationDocumentsWalletPfIdPfDocsGet(id).subscribe({
      next: (value) => {
        console.log(value)
        this.documenti = value;
        this.loading = false;
      },
      error: (err) => {
        this.toastr.error(err.statusText, "Errore nella ricerca!");
      },
      complete: () => console.log(),
    });

  }

  pdfOpen(idDoc: any) {
    let idPf = ""
    if(this.isOPS)
      idPf = String(localStorage.getItem("idPf"))
    else if(this.isPF)
      idPf = this.userService.getUserId()
   this.service.getIdentificationDocumentByIdWalletPfIdPfDocsDocIdGet(idPf, idDoc).subscribe({
     next: value => {

       let url = window.URL.createObjectURL(value);

       let anchor = document.createElement('a');
       anchor.href = url;

       anchor.target = '_blank';
       anchor.click();
     }
   })
  }

   modifica(idDoc: any) {
    localStorage.setItem("idDoc", idDoc);
    this.router.navigateByUrl("/app/doc/updateDoc")
  }

  onClickReferto(idRef: any) {
    localStorage.setItem("idRef", idRef);
  }


  filter() {
    this.getDocs();
  }


  goToPrevious(): void {
    this.page--;
    this.getDocs();
  }
  goToNext(): void {
    this.page++;
    this.getDocs();
  }

  goToPage(n: number): void {
    this.page = n;
    this.getDocs();
  }
}
