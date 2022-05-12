import { Component, OnInit } from '@angular/core';
import {FormArray, FormBuilder, Validators} from "@angular/forms";
import {AuthService} from "../../api/auth.service";
import {PfService} from "../../api/pf.service";
import {DatePipe} from "@angular/common";
import {ToastrService} from "ngx-toastr";
import * as i18nIsoCountries from "i18n-iso-countries";
import {PfInfoWithIdsForUpdate} from "../../model/pfInfoWithIdsForUpdate";
import {Address} from "../../model/address";
import {MaritalStatus} from "../../model/maritalStatus";
import {Citizenship} from "../../model/citizenship";
import {UpdatePfComponent} from "../update-pf/update-pf.component";

@Component({
  selector: 'app-view-anagrafica',
  templateUrl: './view-anagrafica.component.html',
  styleUrls: ['./view-anagrafica.component.css']
})
export class ViewAnagraficaComponent extends UpdatePfComponent{

  override ngOnInit() {
    this.basicSetup();
    this.pfToUpdate = this.authService.getUserId();
    this.loadExistingPf();
    this.PFForm.disable();
  }

}
