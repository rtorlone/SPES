import { ComponentFixture, TestBed } from '@angular/core/testing';

import { PersonaViewComponent } from './persona-view.component';

describe('PersonaViewComponent', () => {
  let component: PersonaViewComponent;
  let fixture: ComponentFixture<PersonaViewComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ PersonaViewComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(PersonaViewComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
