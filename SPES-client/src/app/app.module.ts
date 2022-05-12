import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { LoginComponent } from './login/login.component';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import {MatButtonModule} from "@angular/material/button";
import {MatFormFieldModule} from "@angular/material/form-field";
import {MatInputModule} from "@angular/material/input";
import {MatRippleModule} from "@angular/material/core";
import {FormsModule, ReactiveFormsModule} from "@angular/forms";
import { HttpClientModule, HTTP_INTERCEPTORS } from '@angular/common/http';
import { PfFormComponent } from './pf-form/pf-form.component'
import {MatSelectModule} from "@angular/material/select";
import {MatIconModule} from "@angular/material/icon";
import {MatCheckboxModule} from "@angular/material/checkbox";
import {MatDatepickerModule} from "@angular/material/datepicker";
import {MatCardModule} from "@angular/material/card";
import {MatDividerModule} from "@angular/material/divider";
import {AuthInterceptor} from "./auth/auth.interceptor";
import { ForbiddenComponent } from './forbidden/forbidden.component';
import {MatMomentDateModule} from "@angular/material-moment-adapter";
import { MainDashboardComponent } from './main-dashboard/main-dashboard.component';
import { HomeComponent } from './home/home.component';
import {ToastrModule} from "ngx-toastr";
import { UploadDocComponent } from './upload-doc/upload-doc.component'
import {MatRadioModule} from "@angular/material/radio";
import { UploadComponent } from './upload/upload.component';
import {DatePipe} from "@angular/common";
import { UploadRefertoComponent } from './upload-referto/upload-referto.component';
import { PermissionRequestComponent } from './permission-request/permission-request.component';
import { GetPermissionComponent } from './get-permission/get-permission.component';
import { PaginationComponent } from './pagination/pagination.component';
import { PersoneFragiliComponent } from './persone-fragili/persone-fragili.component';
import { PersonaViewComponent } from './persona-view/persona-view.component';
import { RefertiComponent } from './referti/referti.component';
import { CarrelloComponent } from './carrello/carrello.component';
import { DocumentiComponent } from './documenti/documenti.component';
import { UpdatePfComponent } from './update-pf/update-pf.component';
import { UpdateDocComponent } from './update-doc/update-doc.component';
import { ChangePwdFormComponent } from './change-pwd-form/change-pwd-form.component';
import { ShowCredentialsComponent } from './show-credentials/show-credentials.component';
import { ViewAnagraficaComponent } from './view-anagrafica/view-anagrafica.component';

@NgModule({
  declarations: [
    AppComponent,
    LoginComponent,
    PfFormComponent,
    ForbiddenComponent,
    MainDashboardComponent,
    HomeComponent,
    UploadDocComponent,
    UploadComponent,
    UploadRefertoComponent,
    PermissionRequestComponent,
    GetPermissionComponent,
    PaginationComponent,
    PersoneFragiliComponent,
    PersonaViewComponent,
    RefertiComponent,
    CarrelloComponent,
    DocumentiComponent,
    UpdatePfComponent,
    UpdateDocComponent,
    ChangePwdFormComponent,
    ShowCredentialsComponent,
    ViewAnagraficaComponent,
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    BrowserAnimationsModule,
    MatButtonModule,
    MatFormFieldModule,
    MatInputModule,
    MatRippleModule,
    ReactiveFormsModule,
    FormsModule,
    HttpClientModule,
    MatSelectModule,
    MatIconModule,
    MatCheckboxModule,
    MatDatepickerModule,
    MatCardModule,
    MatDividerModule,
    MatMomentDateModule,
    ToastrModule.forRoot({
      progressBar: true
    }),
    MatRadioModule
  ],
  providers: [{
    provide: HTTP_INTERCEPTORS,
    useClass:AuthInterceptor,
    multi:true
  },
    DatePipe],
  bootstrap: [AppComponent]
})
export class AppModule { }
