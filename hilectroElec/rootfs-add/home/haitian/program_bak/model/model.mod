<?xml version="1.0"?>
<Hilectro version="1.0">
	<model>
		<modelinfo name="test" btnstatus="1000000100"/>
		<btninfo>
			<btn type="动作选择"	no="1"	text="FCW   主臂取出"		>FCW</btn>
			<btn type="动作选择"	no="2"	text="FCS   副臂取出"		>FCS</btn>
			<btn type="动作选择"	no="3"	text="FCTA  取出侧姿势"		con_on1="FCW" con_off1="FCTA2">FCTA</btn>
			<btn type="动作选择"	no="4"	text="FCTA2 取出侧姿势2"	con_on1="FCW" con_off1="FCTA">FCTA2</btn>
			<btn type="动作选择"	no="5"	text="FCTF  去途中开放"		con_on1="FCW" con_off1="FCTB">FCTF</btn>
			<btn type="动作选择"	no="6"	text="FCTB  返回途中开放"	con_on1="FCW" con_off1="FCTF">FCTB</btn>

			<btn type="治具选择"	no="1"	text="FCV1U 使用治具1"		con_on1="FCW">FCV1U</btn>
			<btn type="治具选择"	no="2"	text="FCVC1 治具1确认"		con_on1="FCW,FCV1U">FCVC1</btn>			
			<btn type="治具选择"	no="3"	text="FCV2U 使用治具2"		con_on1="FCW">FCV2U</btn>
			<btn type="治具选择"	no="4"	text="FCVC1 治具2确认"		con_on1="FCW,FCV2U">FCVC2</btn>
			<btn type="治具选择"	no="5"	text="FCV3U 使用治具3"		con_on1="FCW">FCV3U</btn>
			<btn type="治具选择"	no="6"	text="FCVC1 治具3确认"		con_on1="FCW,FCV3U">FCVC3</btn>
			<btn type="治具选择"	no="7"	text="FCV4U 使用治具4"		con_on1="FCW">FCV4U</btn>
			<btn type="治具选择"	no="8"	text="FCVC1 治具4确认"		con_on1="FCW,FCV4U">FCVC4</btn>
			<btn type="治具选择"	no="9"	text="FC4S  料道确认"		con_on1="FCW,FCTF" con_on2="FCW,FCTB">FC4S</btn>

			<btn type="外围动作"	no="1"	text="DEMO1" 				con_on1="FCW" con_off1="FCS">DEMO1</btn>
			<btn type="外围动作"	no="2"	text="DEMO2" 				con_on1="DEMO1">DEMO2</btn>
			<btn type="外围动作"	no="3"	text="DEMO3" 				con_on1="DEMO1">DEMO3</btn>
		</btninfo>
		<program>
			<if condtion="FCW==1 AND (FCTA==1 OR FCTA2==1)">
				<then>
					<c id="LIN2">
						<p n="vel">100</p>
						<p n="acc">100</p>
						<p n="X">P5</p>
						<p n="Y">P5</p>
						<p n="inp">0</p>
					</c>
				</then>
			</if>
			<if condtion="FCW==1 AND FCTA2==1">
				<then>
					<c id="IMI8">
						<p n="in">5564</p>
						<p n="tab">1</p>
						<p n="time">50</p>
					</c>
				</then>
			</if>
			<if condtion="FCW==1">
				<then>
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
				</then>
			</if>
			<if condtion="FCW==1 AND FCTA2==0">
				<then>
					<c id="IMI8">
						<p n="in">5564</p>
						<p n="tab">1</p>
						<p n="time">50</p>
					</c>
				</then>
			</if>
			<if condtion="FCW==1">
				<then>
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
				</then>
			</if>	
			<if condtion="FCW==1 AND FCV1U==1">
				<then>
					<c id="VAC4">
						<p n="out">5603</p>
						<p n="in">5603</p>
						<p n="open">1</p>
						<p n="tab">1</p>
						<p n="chk">1</p>
						<p n="dout">0</p>
						<p n="outd">0</p>
						<p n="time">10</p>
					</c>
				</then>
			</if>
			<if condtion="FCW==1 AND FCV2U==1">
				<then>
					<c id="VAC4">
						<p n="out">5604</p>
						<p n="in">5604</p>
						<p n="open">1</p>
						<p n="tab">1</p>
						<p n="chk">1</p>
						<p n="dout">0</p>
						<p n="outd">0</p>
						<p n="time">10</p>
					</c>
				</then>
			</if>
			<if condtion="FCW==1 AND FCV3U==1">
				<then>
					<c id="VAC4">
						<p n="out">5605</p>
						<p n="in">5605</p>
						<p n="open">1</p>
						<p n="tab">1</p>
						<p n="chk">1</p>
						<p n="dout">0</p>
						<p n="outd">0</p>
						<p n="time">10</p>
					</c>
				</then>
			</if>
			<if condtion="FCW==1 AND FCV4U==1">
				<then>
					<c id="VAC4">
						<p n="out">5606</p>
						<p n="in">5606</p>
						<p n="open">1</p>
						<p n="tab">1</p>
						<p n="chk">1</p>
						<p n="dout">0</p>
						<p n="outd">0</p>
						<p n="time">10</p>
					</c>
				</then>
			</if>
			<if condtion="FCW==1 AND FC4S==1 AND (FCTF==1 OR FCTB==1)">
				<then>
					<c id="VAC4">
						<p n="out">5611</p>
						<p n="in">5611</p>
						<p n="open">1</p>
						<p n="tab">1</p>
						<p n="chk">1</p>
						<p n="dout">0</p>
						<p n="outd">0</p>
						<p n="time">10</p>
					</c>
				</then>
			</if>
			<if condtion="FCW==1">
				<then>
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
				</then>
			</if>
			<if condtion="FCW==1 AND FCTA2==0">
				<then>
					<c id="IMO7">
						<p n="out">5563</p>
						<p n="tab">1</p>
						<p n="time">0</p>
					</c>
				</then>
			</if>
			<if condtion="FCW==1 AND (FCTA==1 OR FCTA2==1)">
				<then>
					<c id="LIN2">
						<p n="vel">100</p>
						<p n="acc">100</p>
						<p n="X">P5</p>
						<p n="Y">P5</p>
						<p n="inp">0</p>
					</c>
					<c id="CHA3">
						<p n="type">1</p>
						<p n="tab">0</p>
						<p n="dout">0</p>
						<p n="outd">0</p>
						<p n="time">10</p>
					</c>
				</then>
			</if>
			<if condtion="FCW==1 AND FCTA2==1">
				<then>
					<c id="IMO7">
						<p n="out">5563</p>
						<p n="tab">1</p>
						<p n="time">0</p>
					</c>
				</then>
			</if>
			<if condtion="FCW==1 AND FCTF==1">
				<then>
					<c id="LIN2">
						<p n="vel">100</p>
						<p n="acc">100</p>
						<p n="X">P6</p>
						<p n="Y">P6</p>
						<p n="inp">0</p>
					</c>
				</then>
			</if>
			<if condtion="FCW==1 AND FCTF==1 AND FCTA==0 AND FCTA2==0">
				<then>
					<c id="CHA3">
						<p n="type">1</p>
						<p n="tab">1</p>
						<p n="dout">0</p>
						<p n="outd">0</p>
						<p n="time">10</p>
					</c>
				</then>
			</if>
			<if condtion="FCW==1 AND FCTF==1">
				<then>
					<c id="POS1">
						<p n="axis">2</p>
						<p n="vel">100</p>
						<p n="acc">100</p>
						<p n="pos">P6</p>
						<p n="inp">0</p>
					</c>
					<c id="VAC4">
						<p n="out">5611</p>
						<p n="in">5611</p>
						<p n="open">0</p>
						<p n="tab">1</p>
						<p n="chk">1</p>
						<p n="dout">0</p>
						<p n="outd">0</p>
						<p n="time">10</p>
					</c>
					<c id="POS1">
						<p n="axis">2</p>
						<p n="vel">100</p>
						<p n="acc">100</p>
						<p n="pos">0</p>
						<p n="inp">0</p>
					</c>
				</then>
			</if>
			<if condtion="FCW==1">
				<then>
					<c id="LIN2">
						<p n="vel">100</p>
						<p n="acc">100</p>
						<p n="X">P4</p>
						<p n="Y">P4</p>
						<p n="inp">0</p>
					</c>
				</then>
			</if>
			<if condtion="FCW==1 AND FCTA==0 AND FCTA2==0 AND FCTF==0">
				<then>
					<c id="CHA3">
						<p n="type">1</p>
						<p n="tab">1</p>
						<p n="dout">0</p>
						<p n="outd">0</p>
						<p n="time">10</p>
					</c>
				</then>
			</if>
			<if condtion="FCW==1">
				<then>
					<c id="POS1">
						<p n="axis">2</p>
						<p n="vel">100</p>
						<p n="acc">100</p>
						<p n="pos">P4</p>
						<p n="inp">0</p>
					</c>
				</then>
			</if>
			<if condtion="FCW==1 AND FCV1U==1">
				<then>
					<c id="VAC4">
						<p n="out">5603</p>
						<p n="in">5603</p>
						<p n="open">0</p>
						<p n="tab">1</p>
						<p n="chk">1</p>
						<p n="dout">0</p>
						<p n="outd">0</p>
						<p n="time">10</p>
					</c>
				</then>
			</if>
			<if condtion="FCW==1 AND FCV2U==1">
				<then>
					<c id="VAC4">
						<p n="out">5604</p>
						<p n="in">5604</p>
						<p n="open">0</p>
						<p n="tab">1</p>
						<p n="chk">1</p>
						<p n="dout">0</p>
						<p n="outd">0</p>
						<p n="time">10</p>
					</c>
				</then>
			</if>
			<if condtion="FCW==1 AND FCV3U==1">
				<then>
					<c id="VAC4">
						<p n="out">5605</p>
						<p n="in">5605</p>
						<p n="open">0</p>
						<p n="tab">1</p>
						<p n="chk">1</p>
						<p n="dout">0</p>
						<p n="outd">0</p>
						<p n="time">10</p>
					</c>
				</then>
			</if>
			<if condtion="FCW==1 AND FCV4U==1">
				<then>
					<c id="VAC4">
						<p n="out">5606</p>
						<p n="in">5606</p>
						<p n="open">0</p>
						<p n="tab">1</p>
						<p n="chk">1</p>
						<p n="dout">0</p>
						<p n="outd">0</p>
						<p n="time">10</p>
					</c>
				</then>
			</if>
			<if condtion="FCW==1">
				<then>
					<c id="POS1">
						<p n="axis">2</p>
						<p n="vel">100</p>
						<p n="acc">100</p>
						<p n="pos">0</p>
						<p n="inp">0</p>
					</c>
				</then>
			</if>
			<if condtion="FCW==1 AND FCTB==1">
				<then>
					<c id="LIN2">
						<p n="vel">100</p>
						<p n="acc">100</p>
						<p n="X">P7</p>
						<p n="Y">P7</p>
						<p n="inp">0</p>
					</c>
					<c id="POS1">
						<p n="axis">2</p>
						<p n="vel">100</p>
						<p n="acc">100</p>
						<p n="pos">P7</p>
						<p n="inp">0</p>
					</c>
					<c id="VAC4">
						<p n="out">5611</p>
						<p n="in">5611</p>
						<p n="open">0</p>
						<p n="tab">1</p>
						<p n="chk">1</p>
						<p n="dout">0</p>
						<p n="outd">0</p>
						<p n="time">10</p>
					</c>
					<c id="POS1">
						<p n="axis">2</p>
						<p n="vel">100</p>
						<p n="acc">100</p>
						<p n="pos">0</p>
						<p n="inp">0</p>
					</c>
				</then>
			</if>
		</program>
	</model>
</Hilectro>
