
classdef Rod < AbsEmbeddedDomain
%%       
    methods (Access = public)
        % constructor
        function obj = Rod(Length)
            obj.Length = Length;
        end
        
       domainIndex = getDomainIndex(obj,Coord)
       visualizeDomain(obj)
    end
    
%%
    properties (Access = private)
        Length
    end
  
end