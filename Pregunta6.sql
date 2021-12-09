drop table nombre;
drop table nueva;
declare    
		@nombre1	varchar(10),
		@nombre2	varchar(10),
		@longitud1  float,
		@longitud2  float,
		@letra		varchar(1),
		@contador	float,
		@sql		nvarchar(2000),
		@columna	varchar(10),
		@mayor		float,
		@auxiliar   float,
		@auxnombre  varchar(10)

set @nombre1='carlos'
set @nombre2='carla'
set @contador=1.0

set @longitud1=LEN(@nombre1)
set @longitud2=LEN(@nombre2)

IF @longitud1 <= @longitud2	set @auxnombre=@nombre1;
IF @longitud1 <= @longitud2	set @nombre1=@nombre2;
IF @longitud1 <= @longitud2	set @nombre2=@auxnombre;

set @longitud1=LEN(@nombre1)
set @longitud2=LEN(@nombre2)

set @sql='create table nombre( '

while @contador<=@longitud1
begin
  set @letra=LEFT(@nombre1,1)
  set @nombre1=RIGHT(@nombre1,LEN(@nombre1)-1)
  set @sql=@sql+@letra+cast(@contador as varchar(1))+' int, '
  set @contador=@contador+1.0
end
set @sql=LEFT(@sql,LEN(@sql)-1)
set @sql=@sql+')'

EXECUTE sp_executesql @sql

set @contador=1.0
while @contador<=@longitud2
begin
  set @letra=LEFT(@nombre2,1)
  set @nombre2=RIGHT(@nombre2,LEN(@nombre2)-1)
  select top 1 @columna=COLUMN_NAME 
  from INFORMATION_SCHEMA.COLUMNS
  where TABLE_NAME='nombre'
  and LEFT(COLUMN_NAME,1)=@letra
  and ORDINAL_POSITION>=@contador
  --set @sql='insert into nombre('+@columna+') values(1)'
  set @sql='insert into nombre('+@letra+cast(@contador as varchar(1))+') values(1)'
  EXECUTE sp_executesql @sql
  print @sql
  set @contador=@contador+1.0
end

set @sql=''
select @mayor=max(ORDINAL_POSITION)
from INFORMATION_SCHEMA.COLUMNS
where TABLE_NAME='nombre'

set @contador=1.0
while @contador<=@mayor
begin
  select @columna=COLUMN_NAME 
  from INFORMATION_SCHEMA.COLUMNS
  where TABLE_NAME='nombre'
  and ORDINAL_POSITION=@contador
  set @sql=@sql+'ISNULL(sum('+@columna+'),0)+'
  set @contador=@contador+1.0
end
set @sql=LEFT(@sql,LEN(@sql)-1)
set @sql='select '+@sql+' as res into nueva from nombre'

EXECUTE sp_executesql @sql

declare @parecido float,
		@mensaje varchar(30)

set @parecido=((select * from nueva)/@longitud1)*100.0
set @mensaje='El parecido entre '+@nombre1+' y '+@nombre2+' es del: '
print @mensaje
print @parecido

select *from nombre