export * from './auth.service';
import { AuthService } from './auth.service';
export * from './pf.service';
import { PfService } from './pf.service';
export * from './report.service';
import { ReportService } from './report.service';
export * from './wallet.service';
import { WalletService } from './wallet.service';
export const APIS = [AuthService, PfService, ReportService, WalletService];
