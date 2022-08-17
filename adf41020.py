

class ADF41020:
    def __init__(self, iface):

        self.iface = iface

        #ref freq in MHz
        self.ref = 100
        #pfd
        self.pfd = 2500

        #adf41020 settings
        self.testmode = 0
        self.CPGain = 0
        self.CPsetting2 = 3
        self.CPsetting1 = 3
        self.CP3state = 0
        self.Prescaler = 2
        self.Timeout = 0
        self.Fastlock = 0
        self.PDPolarity = 0
        self.Muxout = 1 # 0-3state, 1-d lock det,  3-vdd, 7-gnd
        self.Powerdown = 0
        self.CounterReset = 0

        # initial setting
        self.calc_reg(12000)

        # write all regs manually
        self.iface.write_adf(self.Reg0)
        self.iface.write_adf(self.Reg1)
        self.iface.write_adf(self.Reg2)

        # save current setting
        self.last_Reg2 = self.Reg2
        self.last_Reg1 = self.Reg1
        self.last_Reg0 = self.Reg0


    # code stolen from ADI Int-n software :-)
    def calc_reg(self, freq):
        self.fout = freq

        rfout = freq / 4

        self.R = int(self.ref * 1000.0 / self.pfd)
        self.N = int(rfout * 1000.0 / self.pfd)

        self.P = 2**self.Prescaler * 8
        self.B = int(self.N / self.P)
        self.A = int(self.N - self.B * self.P)

        fout_set = 4 * (self.B * self.P + self.A) * self.pfd / 1000.0

        if int(fout_set) != freq:
            print("Warning: requested:", freq, "actual:", fout_set)

        if rfout / self.P > 330.0:
            raise Exception("Warning! Input to the AB counter should be less than 330 MHz.")

        if self.P * self.P - self.P > self.N:
            raise Exception("Warning! For continuously adjacant values of (N * REFin), at output, minimum N value is (P^2 - P)")
        if self.A > self.B:
            raise Exception("Warning! B must be greater than or equal to A. Maybe change the prescaler...")
        if self.B == 0 or self.B == 1 or self.B == 2:
            raise Exception("Warning! B cannot equal 0, 1 or 2.")
        if self.B < self.A:
            raise Exception("Warning! B must be greater than or equal to A.")
        if self.B > 8191:
            raise Exception("Warning! Maximum B value is 8191.")

        self.Reg0 = 1 * 2**23 + 1 * 2**20 + self.testmode * 2**16 + (self.R & 16383) * 2 ** 2
        self.Reg1 = self.CPGain * 2**21 + (self.B & 8191) * 2**8 + (self.A & 63) * 2**2 + 1;
        self.Reg2 = self.Prescaler * 2**22 + self.CPsetting2 * 2**18 + self.CPsetting1 * 2**15 + self.Timeout * 2*11 + self.Fastlock * 2**9 + self.CP3state * 2**8 + self.PDPolarity * 2**7 + self.Muxout * 2**4 + self.Powerdown * 2**3 + self.CounterReset * 2**2 + 2

        return fout_set

    def commit_reg(self):
        if not self.Reg2 == self.last_Reg2:
            self.last_Reg2 = self.Reg2
            self.iface.write_adf(self.Reg2)

        if not self.Reg1 == self.last_Reg1:
            self.last_Reg1 = self.Reg1
            self.iface.write_adf(self.Reg1)

        if not self.Reg0 == self.last_Reg0:
            self.last_Reg0 = self.Reg0
            self.iface.write_adf(self.Reg0)

    def set_freq(self, freq):

        fout_set = self.calc_reg(freq)

        self.commit_reg()

        return fout_set


if __name__ == "__main__": 
    class FakeFx:
        def write_adf(self, word):
            print("write 0x%08x" % word)

    fx = FakeFx()
    adf = ADF41020(fx)


