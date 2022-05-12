import { Component, OnInit } from '@angular/core';
import {HttpClient} from "@angular/common/http";
import {AuthService} from "../../api/auth.service";
import {ToastrService} from "ngx-toastr";
import {PfService} from "../../api/pf.service";
import {Router} from "@angular/router";

@Component({
  selector: 'app-permission-request',
  templateUrl: './permission-request.component.html',
  styleUrls: ['./permission-request.component.css']
})
export class PermissionRequestComponent implements OnInit {

  constructor(private userService: AuthService, private toastr: ToastrService,private pfService: PfService, private router:Router) { }

  ngOnInit(): void {
  }

}
