import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ChangePwdFormComponent } from './change-pwd-form.component';

describe('ChangePwdFormComponent', () => {
  let component: ChangePwdFormComponent;
  let fixture: ComponentFixture<ChangePwdFormComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ ChangePwdFormComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(ChangePwdFormComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
