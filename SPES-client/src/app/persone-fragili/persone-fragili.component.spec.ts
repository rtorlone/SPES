import { ComponentFixture, TestBed } from '@angular/core/testing';

import { PersoneFragiliComponent } from './persone-fragili.component';

describe('PersoneFragiliComponent', () => {
  let component: PersoneFragiliComponent;
  let fixture: ComponentFixture<PersoneFragiliComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ PersoneFragiliComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(PersoneFragiliComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
