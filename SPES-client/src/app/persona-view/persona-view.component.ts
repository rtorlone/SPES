import { Component, OnInit } from '@angular/core';
import {PfService} from "../../api/pf.service";
import {Router} from "@angular/router";
import {AuthService} from "../../api/auth.service";

@Component({
  selector: 'app-persona-view',
  templateUrl: './persona-view.component.html',
  styleUrls: ['./persona-view.component.css']
})
export class PersonaViewComponent implements OnInit {

  persona: any;

  constructor(private userService: PfService, private router: Router, public service: AuthService) {}


    ngOnInit()
    {
      var id = String(localStorage.getItem("idPf"));
      this.userService.getPfInfoByIdPfIdPfGet(id).subscribe({
        next: value => {
          this.persona = value;
        }
      })

    }

  public modificaPersona()
    {
      localStorage.setItem("idPf", this.persona.pf_id);
      this.router.navigateByUrl('app/persona/updateForm');
    }


}
