import { Component } from '@angular/core';
import {AbstractControl, FormBuilder, FormGroup, ValidationErrors, ValidatorFn, Validators} from "@angular/forms";
import {NgxSpinnerService} from "ngx-spinner";
import {ForgetPasswordService} from "../../forget-password/forget-password.service";
import {MatSnackBar} from "@angular/material/snack-bar";
import {ActivatedRoute, Router} from "@angular/router";
import {ToastrService} from "ngx-toastr";

@Component({
  selector: 'app-second-login',
  templateUrl: './second-login.component.html',
  styleUrls: ['./second-login.component.scss']
})
export class SecondLoginComponent {

  token: string = ''

  errorMessages = {
    password: [
      {type: 'required', message: 'Kod jest wymagany'},
    ]
  };

  resetPasswordFrom: FormGroup;

  constructor(
    private spinner: NgxSpinnerService,
    private forgetPasswordService: ForgetPasswordService,
    private _snackBar: MatSnackBar,
    private router: Router,
    formBuilder: FormBuilder,
    private toastr: ToastrService,
    private route: ActivatedRoute,
  ) {
    this.router = router;
    this.resetPasswordFrom = formBuilder.group({
      password: ['', [Validators.required, Validators.minLength(8), Validators.maxLength(30)]],
      confirmPassword: ['', [Validators.required, this.passwordValidator()]],
    });
  }

  ngOnInit(): void {
    this.route.params.subscribe(params => {
      this.token= params['token']
    });
  }

  validationErrors(controlName: string): any[] {
    let errors = []
    // @ts-ignore
    for (let error of this.errorMessages[controlName]) {
      if (this.resetPasswordFrom.get(controlName)?.hasError(error.type)) {
        errors.push(error);
      }
    }
    return errors;
  }

  passwordValidator(): ValidatorFn {
    return (control: AbstractControl): ValidationErrors | null => {
      const passwordToConfirm = control.value;
      const originalPassword = control.parent ? control.parent.get('password')?.value : null;

      if (!passwordToConfirm || !originalPassword) {
        return null; // If the control or country code is empty, consider it valid.
      }

      try {
        if (passwordToConfirm !== originalPassword) {
          return {passwordMismatch: true};
        }
      } catch (error) {
        return {passwordMismatch: true};
      }

      return null;
    };
  }

}
