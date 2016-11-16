import sys
def divide(dividend, divisor):
        """
        :type dividend: int
        :type divisor: int
        :rtype: int
        """
        """
        flag=0
        count=0
        if dividend < 0 and divisor  < 0:
            dividend=-dividend
            divisor=-divisor
        elif dividend < 0 and divisor > 0:
             dividend=-dividend
             flag=1
        elif dividend > 0 and divisor < 0:
             divisor= -divisor
             flag=1

        while dividend >= divisor:
            count=float(count)+1
            print (count)
            dividend=float(dividend)
            dividend-=float(divisor)

        if flag==0:
             count=count

        else:
             count=-count

        return sys.maxsize if count >= sys.maxsize else count
        """

        flag=0
        quotient = 0
        base=1

        if dividend < 0 and divisor  < 0:
            dividend=-dividend
            divisor=-divisor
        elif dividend < 0 and divisor > 0:
             dividend=-dividend
             flag=1
        elif dividend > 0 and divisor < 0:
             divisor= -divisor
             flag=1
        #print (dividend,divisor)
        while  (dividend >= divisor):
            divisor=divisor << 1
            base = base << 1

        while (base > 1):
            divisor >>=1

            base >>=1
            if(dividend >= divisor):
             dividend-=divisor
             quotient+=base



     # Call division recursively

        return quotient if flag==0 else -quotient


print (divide(1,-1))
