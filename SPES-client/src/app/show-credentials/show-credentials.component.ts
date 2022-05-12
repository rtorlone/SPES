import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-show-credentials',
  templateUrl: './show-credentials.component.html',
  styleUrls: ['./show-credentials.component.css']
})
export class ShowCredentialsComponent implements OnInit {
  username:any
  pwd:any
  constructor() { }

  ngOnInit(): void {
    this.username = localStorage.getItem("username")
    this.pwd = localStorage.getItem("pwd")
    localStorage.removeItem("username")
    localStorage.removeItem("pwd")
  }

}
