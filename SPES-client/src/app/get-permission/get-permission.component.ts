import { Component, OnInit } from '@angular/core';
import {HttpClient} from "@angular/common/http";
import {AuthService} from "../../api/auth.service";
import {ToastrService} from "ngx-toastr";
import {PfService} from "../../api/pf.service";
import {Router} from "@angular/router";
import {ReportService} from "../../api/report.service";
import {PermissionToModify} from "../../model/permissionToModify";

@Component({
  selector: 'app-get-permission',
  templateUrl: './get-permission.component.html',
  styleUrls: ['./get-permission.component.css']
})
export class GetPermissionComponent implements OnInit {

  permissions: any
  isPF=this.userService.roleMatch(['PF']);
  permissionsToModify: Array<PermissionToModify> = [];

  constructor(private userService: AuthService, private toastr: ToastrService, private reportService: ReportService, private router: Router) { }

  ngOnInit(): void {
    if (this.isPF == true)
      this.getPermissionAsPF()
  }


  getPermissionAsPF(): void {
    this.reportService.getPermissionsForPfPermissionsGet().subscribe(
      {
        next: value => {
          this.permissions=value;
        },
        error: err => {
          this.toastr.error(err.statusText, "Errore!")
        },
        complete: () => console.log()

      });
  }

  clickReport(idReport: any): void{
    if(localStorage.getItem("onClick")=="true"){
      localStorage.setItem("idReport",idReport);
      this.router.navigateByUrl('app/reportiew');
    }
    localStorage.setItem("onClick","true");
  }



  sendPermission(user_id: any, report_id: any, permission: boolean): void {

    let item: PermissionToModify = {user_id: user_id, report_id: report_id, permission: permission}
    let perms: Array<PermissionToModify> = []
    perms.push(item)

    this.reportService.setMedicalReportsPermissionsPermissionsPatch(perms).subscribe({
      next: value => {
        if(permission){
          this.toastr.success("Permesso concesso", "Success!")
        }
        else {
           this.toastr.success("Permesso negato", "Success!")
        }


      },
      error: err => {
        this.toastr.error(err.statusText, err.status)
      },
      complete:() => {}}

    )
    //window.location.reload();
  }

}
