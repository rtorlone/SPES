import {Component, OnInit, Output, EventEmitter} from '@angular/core';
import {HttpClient, HttpEventType} from '@angular/common/http';
import {WalletService} from "../../api/wallet.service";

@Component({
  selector: 'app-upload',
  templateUrl: './upload.component.html',
  styles: []
})
export class UploadComponent implements OnInit {
  public progress: number = 0;
  public message: string = "";
  @Output() public onUploadFinished = new EventEmitter();

  constructor(private http: HttpClient, private service: WalletService) {
  }

  ngOnInit() {
  }

  public uploadFile = (files: any) => {
    if (files.length === 0) {
      return;
    }

    this.onUploadFinished.emit(Array.from(files as ArrayLike<File>));

  }

}
