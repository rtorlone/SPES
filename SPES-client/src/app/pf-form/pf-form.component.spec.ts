import { ComponentFixture, TestBed } from '@angular/core/testing';

import { PfFormComponent } from './pf-form.component';

describe('PfFormComponent', () => {
  let component: PfFormComponent;
  let fixture: ComponentFixture<PfFormComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ PfFormComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(PfFormComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
