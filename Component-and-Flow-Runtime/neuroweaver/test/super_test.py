class B:
    def method(self, arg):
        print(f"B:{arg}")
        

class C(B):
    def method(self, arg):
        super().method(arg)    # This does the same thing as:
                               # super(C, self).method(arg)
        print(f"after super, C:{arg}")

b = B()
b.method("calling B")

c = C()
c.method("calling C")