import { ComponentFixture, TestBed } from '@angular/core/testing';

import { UploadRefertoComponent } from './upload-referto.component';

describe('UploadRefertoComponent', () => {
  let component: UploadRefertoComponent;
  let fixture: ComponentFixture<UploadRefertoComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ UploadRefertoComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(UploadRefertoComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
