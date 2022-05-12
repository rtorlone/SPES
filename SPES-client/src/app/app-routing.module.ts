import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import {LoginComponent} from "./login/login.component";
import {PfFormComponent} from "./pf-form/pf-form.component";
import {AuthGuard} from "./auth/auth.guard";
import {ForbiddenComponent} from "./forbidden/forbidden.component";
import {MainDashboardComponent} from "./main-dashboard/main-dashboard.component";
import {UploadDocComponent} from "./upload-doc/upload-doc.component";
import {UploadRefertoComponent} from "./upload-referto/upload-referto.component";
import {GetPermissionComponent} from "./get-permission/get-permission.component";
import {PermissionRequestComponent} from "./permission-request/permission-request.component";
import {PersoneFragiliComponent} from "./persone-fragili/persone-fragili.component";
import {PersonaViewComponent} from "./persona-view/persona-view.component";
import {RefertiComponent} from "./referti/referti.component";
import {DocumentiComponent} from "./documenti/documenti.component";
import { UpdatePfComponent} from "./update-pf/update-pf.component";
import {UpdateDocComponent} from "./update-doc/update-doc.component";
import {ChangePwdFormComponent} from "./change-pwd-form/change-pwd-form.component";
import {ShowCredentialsComponent} from "./show-credentials/show-credentials.component";
import {ViewAnagraficaComponent} from "./view-anagrafica/view-anagrafica.component";

const routes: Routes = [
  {path:'',redirectTo:'/login',pathMatch:'full'},
  { path: 'login', component: LoginComponent },
  {path:'forbidden',component :ForbiddenComponent},
  { path:'app',component:MainDashboardComponent,
    children:[ { path: 'insert-pf', component: PfFormComponent, canActivate:[AuthGuard],data:{permittedRoles:['OPS']} },
      { path: 'uploadDoc', component: UploadDocComponent, canActivate:[AuthGuard],data:{permittedRoles:['OPS']} },
      { path: 'uploadReferto', component: UploadRefertoComponent, canActivate:[AuthGuard],data:{permittedRoles:['MED']} },
      { path: 'permissions', component: GetPermissionComponent, canActivate:[AuthGuard],data:{permittedRoles:['PF']} },
      { path: 'permissionRequest', component: PermissionRequestComponent, canActivate:[AuthGuard],data:{permittedRoles:['MED']} },
      { path: 'persone', component: PersoneFragiliComponent,canActivate:[AuthGuard],data:{permittedRoles:['MED', 'OPS']} },
      { path: 'persona/referti', component: RefertiComponent,canActivate:[AuthGuard],data:{permittedRoles:['MED', 'PF']} },
      { path: 'persona/documenti', component: DocumentiComponent,canActivate:[AuthGuard],data:{permittedRoles:['OPS', 'PF']} },
      { path: 'personaView', component: PersonaViewComponent, canActivate:[AuthGuard],data:{permittedRoles:['OPS']}},
      { path: 'persona/updatePf', component: UpdatePfComponent, canActivate:[AuthGuard],data:{permittedRoles:['OPS']}},
      { path: 'doc/updateDoc', component: UpdateDocComponent, canActivate:[AuthGuard],data:{permittedRoles:['OPS']}},
       { path: 'persona/showCredentials', component: ShowCredentialsComponent, canActivate:[AuthGuard],data:{permittedRoles:['OPS']}},
      { path: 'changePwd', component: ChangePwdFormComponent, canActivate:[AuthGuard],data:{permittedRoles:['PF']} },
      { path: 'persona/viewAnagrafica', component: ViewAnagraficaComponent, canActivate:[AuthGuard],data:{permittedRoles:['PF']} },
  ],
    canActivate:[AuthGuard]},
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
