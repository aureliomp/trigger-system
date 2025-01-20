from typing import Union
# import config
from fastapi import FastAPI

# create database structure  function
from scripts.create import DataBase
from scripts.create import DataBase
from scripts.create import Triggers
from scripts.create import Tables
from scripts.create import Procedures
# insert  data into database functions
from scripts.insertions import Media
from scripts.insertions import Enclosure
from scripts.insertions import Settings
from scripts.insertions import Customer

from pydantic import  BaseModel

class DataBases(BaseModel):
    name: str

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

@app.get('/data')
def load_info():
    return  {"message":'''Lo siento.
        Pero... yo no quiero ser emperador. Ese no es mi oficio, sino ayudar a todos si fuera posible. Blancos o negros. Judíos o
        gentiles. Tenemos que ayudarnos los unos a los otros; los seres humanos somos así. Queremos hacer felices a los
        demás, no hacernos desgraciados. No queremos odiar ni despreciar a nadie. En este mundo hay sitio para todos y la
        buena tierra es rica y puede alimentar a todos los seres. El camino de la vida puede ser libre y hermoso, pero lo hemos
        perdido. La codicia ha envenenado las armas, ha levantado barreras de odio, nos ha empujado hacia las miserias y las
        matanzas.
        Hemos progresado muy deprisa, pero nos hemos encarcelado a nosotros mismos. El maquinismo, que crea abundancia,
        nos deja en la necesidad. Nuestro conocimiento nos ha hecho cínicos. Nuestra inteligencia, duros y secos. Pensamos
        demasiado, sentimos muy poco.
        Más que máquinas necesitamos más humanidad. Más que inteligencia, tener bondad y dulzura.
        Sin estas cualidades la vida será violenta, se perderá todo. Los aviones y la radio nos hacen sentirnos más cercanos. La
        verdadera naturaleza de estos inventos exige bondad humana, exige la hermandad universal que nos una a todos
        nosotros.
        Ahora mismo, mi voz llega a millones de seres en todo el mundo, millones de hombres desesperados, mujeres y niños,
        víctimas de un sistema que hace torturar a los hombres y encarcelar a gentes inocentes. A los que puedan oírme, les
        digo: no desesperéis. La desdicha que padecemos no es más que la pasajera codicia y la amargura de hombres que
        temen seguir el camino del progreso humano.
        El odio pasará y caerán los dictadores, y el poder que se le quitó al pueblo se le reintegrará al pueblo, y, así, mientras el
        Hombre exista, la libertad no perecerá.
        Soldados:
        No os entreguéis a ésos que en realidad os desprecian, os esclavizan, reglamentan vuestras vidas y os dicen qué tenéis
        que hacer, qué decir y qué sentir.
        Os barren el cerebro, os ceban, os tratan como a ganado y como carne de cañón. No os entreguéis a estos individuos
        inhumanos, hombres máquina, con cerebros y corazones de máquina.
        Vosotros no sois ganado, no sois máquinas, sois Hombres. Lleváis el amor de la Humanidad en vuestros corazones, no el
        odio. Sólo los que no aman odian, los que nos aman y los inhumanos.
        Soldados:
        No luchéis por la esclavitud, sino por la libertad. En el capítulo 17 de San Lucas se lee: "El Reino de Dios no está en un
        hombre, ni en un grupo de hombres, sino en todos los hombres..." Vosotros los hombres tenéis el poder. El poder de
        crear máquinas, el poder de crear felicidad, el poder de hacer esta vida libre y hermosa y convertirla en una maravillosa
        aventura.
        En nombre de la democracia, utilicemos ese poder actuando todos unidos. Luchemos por un mundo nuevo, digno y
        noble que garantice a los hombres un trabajo, a la juventud un futuro y a la vejez seguridad. Pero bajo la promesa de
        esas cosas, las fieras subieron al poder. Pero mintieron; nunca han cumplido sus promesas ni nunca las cumplirán. Los
        dictadores son libres sólo ellos, pero esclavizan al pueblo. Luchemos ahora para hacer realidad lo prometido. Todos a
        luchar para liberar al mundo. Para derribar barreras nacionales, para eliminar la ambición, el odio y la intolerancia.
        Luchemos por el mundo de la razón.
        Un mundo donde la ciencia, el progreso, nos conduzca a todos a la felicidad.
        Soldados:
        En nombre de la democracia, debemos unirnos todos.
    '''
}

@app.post('/create-structure')
async def data(data: DataBases):
    await DataBase.create(data.name)
    await Tables.create(data.name)
    await Triggers.create(data.name) 
    await Procedures.create(data.name)
    return { 'success': True }
    # return { 'tables':tables }
    
@app.post('/insert-data')
async def  data(data: DataBases):

    await Media.insert(data.name)
    await Enclosure.insertions(data.name)
    await Settings.insertions(data.name)
    await Customer.insertion(data.name)
    return {"status":True}
    
# end def
