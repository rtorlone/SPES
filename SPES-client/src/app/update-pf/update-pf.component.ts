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
import {Address} from "../../model/address";
import {MaritalStatus} from "../../model/maritalStatus";
import {Citizenship} from "../../model/citizenship";
import {PfInfoWithIdsForUpdate} from "../../model/pfInfoWithIdsForUpdate";


@Component({
  selector: 'app-pf-form',
  templateUrl: './update-pf.component.html',
  styleUrls: ['./update-pf.component.css'],
})


export class UpdatePfComponent implements OnInit {

  pfToUpdate: any;

  addressesToDelete: Set<string> = new Set<string>();
  citizenshipsToDelete: Set<string> = new Set<string>();
  maritalStatusesToDelete: Set<string> = new Set<string>();

  date_format: string = 'yyyy-MM-dd';
  maxDate = new Date();

  PFForm = this.fb.group({
    firstname: [null],
    lastname: [null],
    fullname: [null],
    nicknames: [null],
    gender: [null],
    cf: [null, [Validators.maxLength(16), Validators.minLength(16)]],
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
    addresses: this.fb.array([]),
    citizenshipsToAdd: this.fb.array([]),
    maritalStatusesToAdd: this.fb.array([]),
    addressesToAdd: this.fb.array([])
  });

  constructor(private fb: FormBuilder, protected authService: AuthService, private pfService: PfService, private datepipe: DatePipe, private toastr: ToastrService) {
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

    } else {
      this.PFForm.get("is_foreign")?.patchValue(true)
    }
  }

  foreignCheckBoxChange(values: any): void {

    if (values.checked) {
      this.PFForm.get("birth_nation_id")?.patchValue("---")
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


  /* Funzioni per crare le forms */

  createCitizenshipGroup() {
    return this.fb.group({
      id: [],
      nation_id: [null, Validators.required],
      from_date: [Date.now(), Validators.required]
    });
  }

  createCitizenshipGroupToAdd() {
    return this.fb.group({
      nation_id: [null, Validators.required],
      from_date: [Date.now(), Validators.required]
    });
  }

  createMartialsStatusGroup() {
    return this.fb.group({
      id: [],
      marital_status_code: [null, Validators.required],
      from_date: [Date.now(), Validators.required]
    });
  }

  createMartialsStatusGroupToAdd() {
    return this.fb.group({
      marital_status_code: [null, Validators.required],
      from_date: [Date.now(), Validators.required]
    });
  }

  createAddressesForm() {
    return this.fb.group({
      id: [],
      address: [null, Validators.required],
      address_type_id: [null, Validators.required],
      geoarea_id: [null, Validators.required],
      from_date: [Date.now(), Validators.required]
    });
  }

  createAddressesFormToAdd() {
    return this.fb.group({
      address: [null, Validators.required],
      address_type_id: [null, Validators.required],
      geoarea_id: [null, Validators.required],
      from_date: [Date.now(), Validators.required]
    });
  }

  /* Funzioni get per le form */

  get getCitizenshipForm() {
    return this.PFForm.get('citizenship') as FormArray;
  }

  get getCitizenshipFormToAdd() {
    return this.PFForm.get('citizenshipsToAdd') as FormArray;
  }

  get getMartialsStatusForm() {
    return this.PFForm.get('maritalStatus') as FormArray;
  }

  get getMartialsStatusFormToAdd() {
    return this.PFForm.get('maritalStatusesToAdd') as FormArray;
  }

  get getAddressesForm() {
    return this.PFForm.get('addresses') as FormArray;
  }

  get getAddressFormToAdd() {
    return this.PFForm.get('addressesToAdd') as FormArray;
  }

  /* Funzioni per aggiungere form nei formArray */

  addCitizenshipForm() {
    let formCitizenship = this.createCitizenshipGroup()
    this.getCitizenshipForm.push(formCitizenship);
    return formCitizenship;
  }

  addCitizenshipFormToAdd() {
    let formCitizenship = this.createCitizenshipGroupToAdd()
    this.getCitizenshipFormToAdd.push(formCitizenship);
    return formCitizenship;
  }

  addMartialsStatusForm() {
    let formMartialStatus = this.createMartialsStatusGroup()
    this.getMartialsStatusForm.push(formMartialStatus);
    return formMartialStatus;
  }

  addMartialsStatusFormToAdd() {
    let formMartialStatus = this.createMartialsStatusGroupToAdd()
    this.getMartialsStatusFormToAdd.push(formMartialStatus);
    return formMartialStatus;
  }

  addAddressesForm() {
    let formAddress = this.createAddressesForm()
    this.getAddressesForm.push(formAddress);
    return formAddress
  }

  addAddressesFormToAdd() {
    let formAddress = this.createAddressesFormToAdd()
    this.getAddressFormToAdd.push(formAddress);
    return formAddress
  }

  /* Funzioni per rimuovere l'ultima form nei formArray */

  removeCitizenshipFormToAdd() {
    this.getCitizenshipFormToAdd.removeAt(this.getCitizenshipFormToAdd.length - 1)
  }

  removeMaritalStatusFormToAdd() {
    this.getMartialsStatusFormToAdd.removeAt(this.getMartialsStatusFormToAdd.length - 1)
  }

  removeAddressFormToAdd() {
    this.getAddressFormToAdd.removeAt(this.getAddressFormToAdd.length - 1)
  }

  /* Funzioni per rimuovere una specifica form nei formArray.
  * Le form vengono rimosse aggiungendole al set di elminazione ed disabilitandole*/

  removeCitizenshipFormAtIndex(index: number) {
    let form = this.getCitizenshipForm.at(index)
    form.disable()
    this.citizenshipsToDelete.add(form.value.id)
  }

  removeMaritalStatusFormAtIndex(index: number) {
    let form = this.getMartialsStatusForm.at(index)
    form.disable()
    this.maritalStatusesToDelete.add(form.value.id)
  }

  removeAddressFormAtIndex(index: number) {
    let form = this.getAddressesForm.at(index)
    form.disable()
    this.addressesToDelete.add(form.value.id)
  }

  /* Funzioni per aggiungere una specifica form nei formArray.
  * Le form vengono aggiunte rimuovendole dal set di elminazione ed abilitandole*/

  addCitizenshipFormAtIndex(index: number) {
    let form = this.getCitizenshipForm.at(index)
    form.enable()
    this.citizenshipsToDelete.delete(form.value.id)
  }

  addMaritalStatusFormAtIndex(index: number) {
    let form = this.getMartialsStatusForm.at(index)
    form.enable()
    this.maritalStatusesToDelete.delete(form.value.id)
  }

  addAddressFormAtIndex(index: number) {
    let form = this.getAddressesForm.at(index)
    form.enable()
    this.addressesToDelete.delete(form.value.id)
  }

  countriesName: Array<string> = [];
  getAlphaCode = i18nIsoCountries.getAlpha3Code;

  ngOnInit(): void {
    this.basicSetup()
    this.pfToUpdate = localStorage.getItem("idPf");
    this.loadExistingPf()
  }

  basicSetup(): void {
    // @ts-ignore
    i18nIsoCountries.registerLocale(require("i18n-iso-countries/langs/it.json"));
    this.countriesName = Object.values(i18nIsoCountries.getNames("it"));
    this.PFForm.get("death_date")?.disable()
    this.PFForm.get("birth_nation_id")?.patchValue("ITA")
    //this.PFForm.get("birth_nation_id")?.disable()
  }


  onSubmit() {
    let pfInfo: PfInfoWithIdsForUpdate = {
      pf_id: String(localStorage.getItem("idPf")),
      firstname: this.PFForm.get("firstname")?.value,
      lastname: this.PFForm.get("lastname")?.value,
      fullname: this.PFForm.get("fullname")?.value,
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
      address_list_to_update: {},
      marital_status_list_to_update: {},
      citizenship_list_to_update: {},
      address_list_to_delete: [],
      marital_status_list_to_delete: [],
      citizenship_list_to_delete: [],
      address_list_to_add: this.PFForm.get("addressesToAdd")?.value,
      marital_status_list_to_add: this.PFForm.get("maritalStatusesToAdd")?.value,
      citizenship_list_to_add: this.PFForm.get("citizenshipsToAdd")?.value
    };

    /* Prima fase: update e delete */

    this.PFForm.get("addresses")?.value.forEach((elem: any) => {
        if (this.addressesToDelete.has(elem.id))
          return
        let currentAddress: Address = {
          "from_date": String(this.datepipe.transform(elem.from_date, this.date_format)),
          "address": elem.address,
          "geoarea_id": elem.geoarea_id,
          "address_type_id": elem.address_type_id
        };
        Object.assign(pfInfo.address_list_to_update, {[elem.id]: currentAddress})
      }
    )
    this.addressesToDelete.forEach(value => {
      pfInfo.address_list_to_delete?.push(value)
    });

    this.PFForm.get("maritalStatus")?.value.forEach((elem: any) => {
        if (this.maritalStatusesToDelete.has(elem.id))
          return
        let maritalStatus: MaritalStatus = {
          "from_date": String(this.datepipe.transform(elem.from_date, this.date_format)),
          "marital_status_code": elem.marital_status_code
        };
        Object.assign(pfInfo.marital_status_list_to_update, {[elem.id]: maritalStatus})
      }
    )
    this.maritalStatusesToDelete.forEach(value => {
      pfInfo.marital_status_list_to_delete?.push(value)
    });

    this.PFForm.get("citizenship")?.value.forEach((elem: any) => {
        if (this.citizenshipsToDelete.has(elem.id))
          return
        let citizenship: Citizenship = {
          "from_date": String(this.datepipe.transform(elem.from_date, this.date_format)),
          "nation_id": elem.nation_id
        };
        Object.assign(pfInfo.citizenship_list_to_update, {[elem.id]: citizenship})
      }
    )
    this.citizenshipsToDelete.forEach(value => {
      pfInfo.citizenship_list_to_delete?.push(value)
    });

    // Cambio di formato per le restanti date
    pfInfo.address_list_to_add?.forEach(entry => entry.from_date = String(this.datepipe.transform(entry.from_date, this.date_format)))
    pfInfo.marital_status_list_to_add?.forEach(entry => entry.from_date = String(this.datepipe.transform(entry.from_date, this.date_format)))
    pfInfo.citizenship_list_to_add?.forEach(entry => entry.from_date = String(this.datepipe.transform(entry.from_date, this.date_format)))
    if (pfInfo.birth_date != null)
      pfInfo.birth_date = String(this.datepipe.transform(pfInfo.birth_date, this.date_format))
    if (pfInfo.death_date != null)
      pfInfo.death_date = String(this.datepipe.transform(pfInfo.death_date, this.date_format))

    // Esegui l'update
    this.pfService.updatePfInfoByIdPfIdPfPatch(String(localStorage.getItem("idPf")), pfInfo).subscribe(
      {
        next: value => {
          window.location.reload()
          this.toastr.success("PF aggiornata con successo", "PF Aggiornata!")
        },
        error: err => {
          this.toastr.error(err.statusText, "Registrazione Fallita!")
        },
        complete: () => console.log()

      });
  }

  loadExistingPf(): void {

    this.pfService.getPfInfoByIdPfIdPfGet(this.pfToUpdate).subscribe(
      {
        next: value => {

          // Visualizza informazioni generiche.
          this.PFForm.patchValue({
            "firstname": value.firstname,
            "lastname": value.lastname,
            "fullname": value.fullname,
            "nicknames": value.nicknames,
            "cui_code": value.cui_code,
            "cf": value.cf,
            "gender": value.gender,
            "is_anonymous": value.is_anonymous,
            "verified": value.verified,
            "is_foreign": value.is_foreign,
            "birth_date": value.birth_date,
            "birth_city": value.birth_city,
            "birth_geoarea_id": value.birth_geoarea_id,
            "birth_nation_id": value.birth_nation_id,
            "is_dead": value.is_dead,
            "death_date": value.death_date,
          });

          // Visualizza indirizzi
          for (let key in value.address_list) {
            let currentAddress: Address = value.address_list[key]
            this.addAddressesForm().patchValue({
              "id": key,
              "address": currentAddress.address,
              "geoarea_id": currentAddress.geoarea_id,
              "address_type_id": currentAddress.address_type_id,
              "from_date": currentAddress.from_date
            });
          }
          ;

          // Visualizza Marital Status
          for (let key in value.marital_status_list) {
            let currentMaritalStatus: MaritalStatus = value.marital_status_list[key]
            this.addMartialsStatusForm().patchValue({
              "id": key,
              "marital_status_code": currentMaritalStatus.marital_status_code,
              "from_date": currentMaritalStatus.from_date
            });
          }
          ;

          // Visualizza Cittadinanze
          for (let key in value.citizenship_list) {
            let currentCitizenship: Citizenship = value.citizenship_list[key]
            this.addCitizenshipForm().patchValue({
              "id": key,
              "nation_id": currentCitizenship.nation_id,
              "from_date": currentCitizenship.from_date
            });
          }
          ;

        },
        error: err => {
          this.toastr.error(err.statusText, "Errore!")
        },
        complete: () => console.log()

      });
  }
}
