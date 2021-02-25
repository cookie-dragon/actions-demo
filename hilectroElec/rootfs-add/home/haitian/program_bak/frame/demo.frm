<?xml version='1.0' encoding='UTF-8'?>
<Hilectro version="1.0">
    <model>
        <modelinfo btnstatus="1000000000000000000000000000000000000000000" name="$model.xml"/>
    </model>
    <info>
        <Axismask>7</Axismask>
        <ProductionSet>0</ProductionSet>
        <RejectsSet>0</RejectsSet>
        <Onceout>1</Onceout>
        <Production>0</Production>
        <Rejects>0</Rejects>
        <Robperiod>13.68</Robperiod>
        <Tasktime>3.85</Tasktime>
    </info>
    <program>
        <c id="CHA3">
            <p n="type">0</p>
            <p n="tab">1</p>
            <p n="dout">0</p>
            <p n="outd">0</p>
            <p n="time">10</p>
        </c>
        <c id="LIN2">
            <p n="vel">100</p>
            <p n="acc">100</p>
            <p n="X">P1</p>
            <p n="Y">P1</p>
            <p n="Z">P1</p>
            <p n="inp">0</p>
        </c>
        <c id="IMI8">
            <p n="in">5564</p>
            <p n="tab">1</p>
            <p n="time">50</p>
        </c>
        <c id="POS1">
            <p n="axis">2</p>
            <p n="vel">100</p>
            <p n="acc">100</p>
            <p n="pos">P2</p>
            <p n="inp">0</p>
        </c>
        <c id="POS1">
            <p n="axis">1</p>
            <p n="vel">100</p>
            <p n="acc">100</p>
            <p n="pos">P2</p>
            <p n="inp">0</p>
        </c>
        <c id="POS1">
            <p n="axis">1</p>
            <p n="vel">100</p>
            <p n="acc">100</p>
            <p n="pos">P3</p>
            <p n="inp">0</p>
        </c>
        <c id="POS1">
            <p n="axis">2</p>
            <p n="vel">100</p>
            <p n="acc">100</p>
            <p n="pos">0</p>
            <p n="inp">0</p>
        </c>
        <c id="IMO7">
            <p n="out">5563</p>
            <p n="tab">1</p>
            <p n="time">0</p>
        </c>
        <c id="LIN2">
            <p n="vel">100</p>
            <p n="acc">100</p>
            <p n="X">P4</p>
            <p n="Y">P4</p>
            <p n="inp">0</p>
        </c>
        <c id="CHA3">
            <p n="type">1</p>
            <p n="tab">1</p>
            <p n="dout">0</p>
            <p n="outd">0</p>
            <p n="time">10</p>
        </c>
        <c id="POS1">
            <p n="axis">2</p>
            <p n="vel">100</p>
            <p n="acc">100</p>
            <p n="pos">P4</p>
            <p n="inp">0</p>
        </c>
        <c id="POS1">
            <p n="axis">2</p>
            <p n="vel">100</p>
            <p n="acc">100</p>
            <p n="pos">0</p>
            <p n="inp">0</p>
        </c>
        <c id="END0"/>
    </program>
    <data>
        <position>
            <pos num="1" active="3">
                <p n="1">0</p>
                <p n="1">0</p>
                <p n="1">0</p>
                <p n="0">0</p>
                <p n="0">0</p>
                <p n="0">0</p>
                <p n="0">0</p>
                <p n="0">0</p>
                <p n="v">100</p>
                <p n="a">100</p>
            </pos>
            <pos num="2" active="2">
                <p n="0">0</p>
                <p n="1">0</p>
                <p n="1">0</p>
                <p n="0">0</p>
                <p n="0">0</p>
                <p n="0">0</p>
                <p n="0">0</p>
                <p n="0">0</p>
                <p n="v">100</p>
                <p n="a">100</p>
            </pos>
            <pos num="3" active="1">
                <p n="0">0</p>
                <p n="1">0</p>
                <p n="0">0</p>
                <p n="0">0</p>
                <p n="0">0</p>
                <p n="0">0</p>
                <p n="0">0</p>
                <p n="0">0</p>
                <p n="v">100</p>
                <p n="a">100</p>
            </pos>
            <pos num="4" active="3">
                <p n="1">0</p>
                <p n="1">0</p>
                <p n="1">0</p>
                <p n="0">0</p>
                <p n="0">0</p>
                <p n="0">0</p>
                <p n="0">0</p>
                <p n="0">0</p>
                <p n="v">100</p>
                <p n="a">100</p>
            </pos>
        </position>
        <io>
            <class type="vac">
                <port out="5602" active="2">
                    <p n="in">5602</p>
                    <p n="odly">0</p>
                    <p n="oexc">0</p>
                    <p n="otim">10</p>
                    <p n="ochk">1</p>
                    <p n="cdly">0</p>
                    <p n="cexc">0</p>
                    <p n="ctim">10</p>
                    <p n="cchk">1</p>
                </port>
            </class>
            <class type="imo">
                <port out="5563" active="1">
                    <p n="odly">0</p>
                </port>
            </class>
            <class type="imi">
                <port in="5564" active="1">
                    <p n="tout">50</p>
                </port>
            </class>
        </io>
        <timer>
            <t num="1" active="0">1</t>
        </timer>
        <counter>
            <cnt num="1" active="0">1</cnt>
        </counter>
        <matrix>
            <mtx num="1" active="0">
                <chamfer>0</chamfer>
                <xseq>1</xseq>
                <yseq>2</yseq>
                <xnum>1</xnum>
                <ynum>1</ynum>
                <znum>1</znum>
                <xdist>0</xdist>
                <ydist>0</ydist>
                <zdist>0</zdist>
                <xfrist>0</xfrist>
                <yfrist>0</yfrist>
                <zfrist>0</zfrist>
                <vel>100</vel>
                <acc>100</acc>
                <vlow>20</vlow>
                <ddist>0</ddist>
            </mtx>
        </matrix>
        <fpack>
            <pack num="1" active="0">
                <pnum>1</pnum>
                <chamfer>0</chamfer>
                <vel>100</vel>
                <acc>100</acc>
                <vlow>20</vlow>
                <ddist>0</ddist>
                <pos>
                    <p x="0" y="0" z="0">1</p>
                </pos>
            </pack>
        </fpack>
    </data>
</Hilectro>
