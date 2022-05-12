import { Component, OnInit } from '@angular/core';
import { FormBuilder, Validators, FormGroup } from '@angular/forms';
import { AuthService } from "../../api/auth.service";
import { Router } from '@angular/router';
import { ToastrService } from 'ngx-toastr';
import {PfService} from "../../api/pf.service";
import {PfInfoWithIdsForUpdate} from "../../model/pfInfoWithIdsForUpdate";
import {UserInfoWithPwd} from "../../model/userInfoWithPwd";
import {UserInfoForUpdate} from "../../model/userInfoForUpdate";

@Component({
  selector: 'app-change-pwd-form',
  templateUrl: './change-pwd-form.component.html',
  styles: []
})
export class ChangePwdFormComponent implements OnInit {

  constructor( private toastr:ToastrService, private fb:FormBuilder,private userService:AuthService,private router:Router, private service: PfService) { }
  formModel=this.fb.group({

    OldPassword :[''],
    Passwords:this.fb.group({
    NewPassword :['',[Validators.required,Validators.minLength(4)]],
    ConfirmNewPassword:['',Validators.required]},
    {validator:this.comparePasswords})



  });
  ngOnInit() {
  }
  comparePasswords( fb:FormGroup){
    let confirmPwdCtrl = fb.get('ConfirmNewPassword');
    //pwdMismatch
    // @ts-ignore
    if(confirmPwdCtrl.errors==null || 'passwordMismatch' in confirmPwdCtrl.errors){
      // @ts-ignore
      if(fb.get('NewPassword').value!= confirmPwdCtrl.value)
      { // @ts-ignore
        confirmPwdCtrl.setErrors({passwordMismatch:true})
      }
      else
      { // @ts-ignore
        confirmPwdCtrl.setErrors(null)
      }
    }
}
onSubmit(){
    let id_pf = this.userService.getUserId()
    var body: UserInfoForUpdate = {
    old_pwd: this.formModel.value.OldPassword,
    new_pwd: this.formModel.value.Passwords.NewPassword
  };
  this.service.updatePfUserInfoUserPfPatch( body).subscribe({


    next: value =>{

       this.toastr.success("Password modificata!","La Modifica ha avuto successo.");

    },
    error: err => {
         this.toastr.error(err.statusText,err.status);
    },
    complete: () => {

    }

    }
  );
  this.formModel.reset()



}

}

