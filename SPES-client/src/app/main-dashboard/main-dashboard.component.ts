import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import {AuthService} from "../../api/auth.service";

@Component({
  selector: 'app-main-dashboard',
  templateUrl: './main-dashboard.component.html',
  styleUrls: ['./main-dashboard.component.css']
})
export class MainDashboardComponent implements OnInit {

  constructor(private router:Router, public service: AuthService) { }

  ngOnInit() {
  }
  onLogout(){
    localStorage.removeItem('jwt_token');
    localStorage.clear()
    this.router.navigate(['/login'])
  }
}
