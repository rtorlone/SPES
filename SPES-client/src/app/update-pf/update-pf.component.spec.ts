import { ComponentFixture, TestBed } from '@angular/core/testing';

import { UpdatePfComponent } from './update-pf.component';

describe('UpdatePfComponent', () => {
  let component: UpdatePfComponent;
  let fixture: ComponentFixture<UpdatePfComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ UpdatePfComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(UpdatePfComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
