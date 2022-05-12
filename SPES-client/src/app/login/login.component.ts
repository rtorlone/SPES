import {Component, OnInit} from '@angular/core';
import {AuthService} from '../../api/auth.service';
import {FormControl, FormGroupDirective, NgForm} from "@angular/forms";
import {ErrorStateMatcher} from "@angular/material/core";
import {Login} from "../../model/login";
import {Router} from '@angular/router';
import {ToastrService} from "ngx-toastr";

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})

export class LoginComponent implements OnInit {
  formModel: any = {
    username: null,
    password: null
  };
  isLoggedIn = false;
  isLoginFailed = false;
  errorMessage = '';
  roles: string[] = [];

  //private tokenStorage: TokenStorageService
  constructor(private authService: AuthService, private router: Router, private toastr: ToastrService) {
  }

  ngOnInit(): void {
    //if (this.tokenStorage.getToken()) {
    // this.isLoggedIn = true;
    //  this.roles = this.tokenStorage.getUser().roles;
    //console.log(this.authService.roleMatch(["OPS"]))

    //console.log(this.authService.isLoggedIn())
  }

//}
  onSubmit(): void {
    const {username, password} = this.formModel;
    let login: Login = {username, password}

    this.authService.authAuthPost(login).subscribe(
      {

        next: value => {
          console.log(value);
          this.authService.setSession(String(value.jwt), String(value.expires_at))
          if (this.authService.roleMatch(['OPS'])) {
            this.router.navigateByUrl('/app/persone');
          } else if (this.authService.roleMatch(['MED'])) {
            this.router.navigateByUrl('/app/persone');
          } else if (this.authService.roleMatch(['PF'])) {
            if (value.first_access)
              this.router.navigateByUrl('/app/changePwd');
            else
              this.router.navigateByUrl('/app/permissions');
          }
        },
        error: err => {
          console.log(err);
          console.log(err.statusText);
          this.toastr.error('Incorrect Username or password', 'Authentication Failed.');
        },
        complete: () => console.log()

      });
  }

  reloadPage(): void {
    window.location.reload();
  }
}

/** Error when invalid control is dirty, touched, or submitted. */
export class MyErrorStateMatcher implements ErrorStateMatcher {
  isErrorState(control: FormControl | null, form: FormGroupDirective | NgForm | null): boolean {
    const isSubmitted = form && form.submitted;
    return !!(control && control.invalid && (control.dirty || control.touched || isSubmitted));
  }
}
