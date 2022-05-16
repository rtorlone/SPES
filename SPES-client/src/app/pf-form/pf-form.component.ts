import {Component, OnInit} from '@angular/core';
import {AuthService} from "../../api/auth.service";
import {PfService} from "../../api/pf.service";
import {PfInfo} from "../../model/pfInfo";
import {FormArray, FormBuilder, Validators} from "@angular/forms";
import * as i18nIsoCountries from "i18n-iso-countries";
import {DateAdapter, MAT_DATE_FORMATS, MAT_DATE_LOCALE} from '@angular/material/core';
import 'moment/locale/it';
import {DatePipe} from "@angular/common";
import {ToastrService} from "ngx-toastr";
import {Router} from "@angular/router";


@Component({
  selector: 'app-pf-form',
  templateUrl: './pf-form.component.html',
  styleUrls: ['./pf-form.component.css'],
})


export class PfFormComponent implements OnInit {

  date_format: string = 'yyyy-MM-dd';
  maxDate = new Date();

  PFForm = this.fb.group({
    firstname: [null],
    lastname: [null],
    fullname: [null],
    email: [null, Validators.email],
    nicknames: [null],
    gender: [null],
    cf: [null, [Validators.maxLength(16),Validators.minLength(16)]],
    cui_code: [null],
    is_anonymous: [false],
    verified: [true],
    is_foreign: [false],
    is_dead: [false],
    birth_date: [null],
    birth_nation_id: [null],
    birth_geoarea_id: [null],
    birth_city: [null],
    death_date: [null],
    citizenship: this.fb.array([]),
    maritalStatus: this.fb.array([]),
    addresses: this.fb.array([])
  });

  constructor(private router:Router,private fb: FormBuilder, private authService: AuthService, private pfService: PfService, private datepipe: DatePipe, private toastr: ToastrService) {
  }


  /**
   * Questa funzione a seconda del valore della checkbox "anonymous disattiva o attiva gli input form relativi al firstname e lastname"
   **/
  anonymousCheckBoxChange(values: any): void {

    if (values.checked) {
      this.PFForm.get("firstname")?.disable()
      this.PFForm.get("lastname")?.disable()
      this.PFForm.patchValue({"firstname": null, "lastname": null})
    } else {
      this.PFForm.get("firstname")?.enable()
      this.PFForm.get("lastname")?.enable()
    }
  }

  nationIdChange(values: any): void {

    if (values.value == "ITA") {
      this.PFForm.get("is_foreign")?.patchValue(false)

    }
    else{
      this.PFForm.get("is_foreign")?.patchValue(true)
    }
  }

  foreignCheckBoxChange(values: any): void {

    if (values.checked) {
      this.PFForm.get("birth_nation_id")?.patchValue(null)
      //this.PFForm.get("birth_nation_id")?.enable()
    } else {
      this.PFForm.get("birth_nation_id")?.patchValue("ITA")
      //this.PFForm.get("birth_nation_id")?.disable()
    }
  }

  deadCheckBoxChange(values: any): void {
    if (values.checked) {
      this.PFForm.get("death_date")?.enable()
    } else {
      this.PFForm.get("death_date")?.disable()
      this.PFForm.get("death_date")?.patchValue(null)
    }
  }


  /* Citizenship Form */

  createCitizenshipGroup() {
    return this.fb.group({
      nation_id: [null, Validators.required],
      from_date: [Date.now(), Validators.required]
    });
  }

  get getCitizenshipForm() {
    return this.PFForm.get('citizenship') as FormArray;
  }

  addCitizenshipForm() {
    this.getCitizenshipForm.push(this.createCitizenshipGroup());
  }

  removeCitizenshipForm() {
    this.getCitizenshipForm.removeAt(this.getCitizenshipForm.length - 1)
  }

  /* Marital Status Form */

  createMartialsStatusGroup() {
    return this.fb.group({
      marital_status_code: [null, Validators.required],
      from_date: [Date.now(), Validators.required]
    });
  }

  get getMartialsStatusForm() {
    return this.PFForm.get('maritalStatus') as FormArray;
  }

  addMartialsStatusForm() {
    this.getMartialsStatusForm.push(this.createMartialsStatusGroup());
  }

  removeMartialsStatusForm() {
    this.getMartialsStatusForm.removeAt(this.getMartialsStatusForm.length - 1)
  }

  /* Addresses Form */

  createAddressesForm() {
    return this.fb.group({
      address: [null, Validators.required],
      address_type_id: [null, Validators.required],
      geoarea_id: [null, Validators.required],
      from_date: [Date.now(), Validators.required]
    });
  }

  get getAddressesForm() {
    return this.PFForm.get('addresses') as FormArray;
  }

  addAddressesForm() {
    this.getAddressesForm.push(this.createAddressesForm());
  }

  removeAddressesForm() {
    this.getAddressesForm.removeAt(this.getAddressesForm.length - 1)
  }

  countriesName: Array<string> = [];
  getAlphaCode = i18nIsoCountries.getAlpha3Code;

  ngOnInit(): void {
    // @ts-ignore
    i18nIsoCountries.registerLocale(require("i18n-iso-countries/langs/it.json"));
    this.countriesName = Object.values(i18nIsoCountries.getNames("it"));
    this.PFForm.get("death_date")?.disable()
    this.PFForm.get("birth_nation_id")?.patchValue("ITA")
    //this.PFForm.get("birth_nation_id")?.disable()
  }

  onSubmit() {
    let pfInfo: PfInfo = {
     firstname: this.PFForm.get("firstname")?.value,
      lastname: this.PFForm.get("lastname")?.value,
      fullname: this.PFForm.get("fullname")?.value,
      email: this.PFForm.get("email")?.value,
      nicknames: this.PFForm.get("nicknames")?.value,
      cf: this.PFForm.get("cf")?.value,
      cui_code: this.PFForm.get("cui_code")?.value,
      gender: this.PFForm.get("gender")?.value,
      birth_date: this.PFForm.get("birth_date")?.value,
      birth_city: this.PFForm.get("birth_city")?.value,
      birth_nation_id: this.PFForm.get("birth_nation_id")?.value,
      birth_geoarea_id: this.PFForm.get("birth_geoarea_id")?.value,
      is_dead: this.PFForm.get("is_dead")?.value,
      death_date: this.PFForm.get("death_date")?.value,
      is_anonymous: this.PFForm.get("is_anonymous")?.value,
      is_foreign: this.PFForm.get("is_foreign")?.value,
      address_list: this.PFForm.get("addresses")?.value,
      marital_status_list: this.PFForm.get("maritalStatus")?.value,
      citizenship_list: this.PFForm.get("citizenship")?.value,
    };

    // Cambio di formato di tutte le date
    pfInfo.address_list?.forEach(entry => entry.from_date = String(this.datepipe.transform(entry.from_date, this.date_format)))
    pfInfo.marital_status_list?.forEach(entry => entry.from_date = String(this.datepipe.transform(entry.from_date, this.date_format)))
    pfInfo.citizenship_list?.forEach(entry => entry.from_date = String(this.datepipe.transform(entry.from_date, this.date_format)))
    if (pfInfo.birth_date != null)
      pfInfo.birth_date = String(this.datepipe.transform(pfInfo.birth_date, this.date_format))
    if (pfInfo.death_date != null)
      pfInfo.death_date = String(this.datepipe.transform(pfInfo.death_date, this.date_format))

    // Esegui la registrazione
    this.pfService.registerPfPfPost(pfInfo).subscribe(
      {
        next: value => {
          this.toastr.success("PF inserita con successo", "PF Registrata!")
          localStorage.setItem("username",value["username"])
          localStorage.setItem("pwd", value["password"])
          this.router.navigateByUrl("app/persona/showCredentials")
        },
        error: err => {
          this.toastr.error(err.statusText, "Registrazione Fallita!")
        },
        complete: () => console.log()

      });
  }
}
