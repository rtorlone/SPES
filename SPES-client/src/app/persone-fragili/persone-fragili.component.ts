import { Component, OnInit, EventEmitter, Output } from '@angular/core';
import { PfService } from "../../api/pf.service";
import { Router } from '@angular/router';
import { ToastrService } from 'ngx-toastr';
import { AuthService } from "../../api/auth.service";
import {HttpClient} from "@angular/common/http";

@Component({
  selector: 'app-persone-fragili',
  templateUrl: './persone-fragili.component.html',
  styleUrls: ['./persone-fragili.component.css']
})
export class PersoneFragiliComponent implements OnInit {
  // @ts-ignore
  persone;
  current="noFilter";
  radioOption="nome";
  secondOption="cognome";
  isOPS=this.userService.roleMatch(['OPS']);
  isMED=this.userService.roleMatch(['MED']);
  searchText :string="";
  searchText2:string="";
  searchText3:string="";
  nome="Persone";
  page=1;
  total=0;
  limit=100;
// @ts-ignore
  totalPages;
  loading =false;
  @Output() public personaEmitter= new EventEmitter();

  constructor(private http: HttpClient,private userService:AuthService, private toastr:ToastrService,private service:PfService,private router:Router) { }

  ngOnInit() {
 this.getPersone();

  }
  // @ts-ignore
  onSubmit(e){
    console.log("submit")

  }
  clearFilter(){
    this.searchText="";
  }
  clearFilter2(){
    this.searchText2="";
  }
 clearFilter3(){
    this.searchText3="";
  }

  getPersone():void{
    console.log("getPersone")
    /*if(this.current=="filter"){
    this.service.getStrumenti(this.page,this.limit,this,this.searchText,this.secondOption,this.searchText2).subscribe(
      res=>{
        this.strumenti=res.page.data;
        this.total=res.page.total;
        this.loading=false;
      },
      err=>{
        console.log(err);
      }
    );}
    else if(this.current=="noFilter"){
      *//*this.http.get("http://localhost:8080/search/pf?firstname=" + this.searchText + "&lastname=" + this.searchText2).subscribe(
        value=>{
          this.persone=value;
          this.loading=false;

        });*//*
    }
    else if(this.current=="singleFilter"){
      this.service.getStrumentiSingleFilter(this.page,this.limit,this.radioOption,this.searchText).subscribe(
        res=>{
          this.strumenti=res.page.data;
          this.total=res.page.total;
          this.loading=false;
        },
        err=>{
          console.log(err);
        }

    );


    }*/
    console.log(this.searchText2, this.searchText)
    this.service.searchPfsByQuerySearchPfGet(this.searchText, this.searchText2, this.searchText3).subscribe(
      {
        next: value => {
          this.persone=value;
          this.loading=false;
        },
        error: err => {
          this.persone= []
          this.toastr.error(err.statusText, "Errore nella ricerca!")

        },
        complete: () => console.log()

      });


  }

  filter(){
    if(this.searchText==""&&this.searchText2==""){
     this.current="noFilter";
    this.getPersone();
  }
  else if(this.searchText2==""){
    this.current="singleFilter";
    this.getPersone();
  }
  else{
    this.current="filter";
    this.getPersone();
  }

  }

  // @ts-ignore
  pdfOpen(path){
    localStorage.setItem("onClick","false");
    window.open('https://localhost:8080/'+path,'_blank');

    this.router.navigateByUrl('app/strumento/strumenti');

  }
  // @ts-ignore
  getDocs(idPf){
    localStorage.setItem("idPf",idPf);
     this.router.navigateByUrl('app/persona/documenti');

  }
  // @ts-ignore
  addReferto(idPf){
    localStorage.setItem("idPf",idPf);
    this.router.navigateByUrl('app/uploadReferto');
  }
   // @ts-ignore
  addDoc(idPf){
    localStorage.setItem("idPf",idPf);
    this.router.navigateByUrl('app/uploadDoc');
  }
  // @ts-ignore
  onClickPersona(idPf){
    if(localStorage.getItem("onClick")=="true"){
    console.log(idPf);
    localStorage.setItem("idPf",idPf);
    console.log("baaaaah");
    this.router.navigateByUrl('app/personaView');
    }
    localStorage.setItem("onClick","true");
  }
   // @ts-ignore
  public modificaPersona(idPf)
    {
      localStorage.setItem("idPf", idPf);
      this.router.navigateByUrl('app/persona/updatePf');
    }

     // @ts-ignore
  public getReports(idPf)
    {
      localStorage.setItem("idPf", idPf);
      this.router.navigateByUrl('app/persona/referti');
    }
  goToPrevious() :void{
    this.page--;
    this.getPersone();
  }
  goToNext() :void{
    this.page++;
    this.getPersone();
  }

  goToPage(n:number):void{
    this.page=n;
    this.getPersone();
  }


}
