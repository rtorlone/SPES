import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ViewAnagraficaComponent } from './view-anagrafica.component';

describe('ViewAnagraficaComponent', () => {
  let component: ViewAnagraficaComponent;
  let fixture: ComponentFixture<ViewAnagraficaComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ ViewAnagraficaComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(ViewAnagraficaComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
