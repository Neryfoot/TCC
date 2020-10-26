function  [sys,x0,str,ts]  = modulos_opc(t,x,u,flag,dt,machine,server,tagin,tagout)

% Função que envia o sinal de entrada "u" para o canal de entrada (bomba) 
% e faz leituras através de comunicação com servidor OPC.
% Parâmetros:
% dt : tempo de amostragem em segundos
% machine : string contendo o alias do computador onde esta o servidor OPC (p.ex., 'localhost', '\\HOST'
% server : string contendo o nome do servidor de OPC (p.ex.,'Servidor.OPC.1')
% tagin : string contendo o nome da variavel de escrita (entrada da planta/varável manipulada), p.ex., 'bomba1.op'
% tagout: string contendo o nome da variavel de leitura (saída da planta/variável controlada), p.ex.,  'vazao1.pv'

% Pedro Rafael Fernandes
% 17-Out-2012

persistent time0;

if abs(flag) == 2	      
   
   if u < 0
      u = 0;
   end
   
   % Acionamento das Bombas
   
   da = opcda(machine, server);
   connect(da);
   grp = addgroup(da);
   itm = additem(grp, tagin);
   write(itm,u(1));       % Bomba Selecionada pelo parâmetro de entrada "tagin"
   
   while etime(clock,x') < dt; end
   
   sys = clock;
   
   disconnect(da)
   delete(da)
   
elseif flag == 4
   
   sys = [];
   
elseif flag == 0
   
   sys(1) = 0;                               % Número de Estados Contínuos
   sys(2) = size(clock,2);                   % Número de Estados Discretos
   sys(3) = 3;                               % Número de Saídas
   sys(4) = 1;                               % Número de Entradas
   sys(5) = 0;
   sys(6) = 0;
   sys(7) = 1;                               % Tempo de Amostragem
   
   x0    = clock;
   time0 = 60*(60*x0(4) + x0(5)) + x0(6);
   str   = [];
   ts    = [dt, 0];
   
elseif flag == 3
   
    sys(1) = 60*(60*x(4) + x(5)) + x(6) - time0;                                       % Tempo ------ (Segundos)

      
   % retornando sinal de saída
   da = opcda(machine, server);
   connect(da);
   grp = addgroup(da);
   itm = additem(grp, tagout);
   tic;
   val = read(itm);      % Sensor Selecionado pelo parâmetro de entrada "tagout"
   sys(3) = toc;
   sys(2) = val.Value;
   disconnect(da)
   delete(da)

else 
   
   sys    = [];
   
end