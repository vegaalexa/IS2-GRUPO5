create or replace function F_TR_ACTUALIZAR_ESTADO() returns Trigger
as
$$
declare
	nv_cant_sprint integer:=0;
	nv_cant_finalizado integer:=0;
	cur_proyectos CURSOR FOR SELECT * FROM "Proyecto" where "estado"<>'F'; 
begin
	FOR reg IN cur_proyectos LOOP
		--Cantidad de SprintBacklogs por proyecto
		select count(*) 
		into nv_cant_sprint
		from "Proyecto" p
		join "BackLog" b on p."idProyecto"= b."proyecto_id"
		left join "SprintBackLog" sb on b."idBackLog"=sb."backLog_id"
		where p."estado"<>'F' and p."idProyecto"=reg."idProyecto";

		--Cantidad de SB finalizados
		select count(*) 
		into nv_cant_finalizado
		from "Proyecto" p
		join "BackLog" b on p."idProyecto"= b."proyecto_id"
		join "SprintBackLog" sb on b."idBackLog"=sb."backLog_id"
		where sb."estado"='F' and p."idProyecto"=reg."idProyecto";
		
		if (nv_cant_sprint<>0 and nv_cant_finalizado<>0) and nv_cant_sprint=nv_cant_finalizado then
			UPDATE public."Proyecto" SET "estado"='F' where "idProyecto"=reg."idProyecto";
		end if;
	end loop;
	return new;
End
$$
Language plpgsql;
/

create or replace trigger TR_ACTUALIZAR_ESTADO_PROYECTO after update on "SprintBackLog"
for each row
execute procedure F_TR_ACTUALIZAR_ESTADO();
/