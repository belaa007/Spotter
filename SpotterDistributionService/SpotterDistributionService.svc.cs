using System;

namespace SpotterDistributionService
{
    // NOTE: You can use the "Rename" command on the "Refactor" menu to change the class name "Service1" in code, svc and config file together.
    // NOTE: In order to launch WCF Test Client for testing this service, please select Service1.svc or Service1.svc.cs at the Solution Explorer and start debugging.
    public class Service1 : ISpotterDistributionService
    {

        public SpotterDataTransferObject.PingResult Ping(SpotterDataTransferObject.PingParameter parameter)
        {
            throw new NotImplementedException();
        }

        public SpotterDataTransferObject.FPingResult FPing(SpotterDataTransferObject.FPingParameter parameter)
        {
            throw new NotImplementedException();
        }

        public SpotterDataTransferObject.UpdateResult Update(SpotterDataTransferObject.UpdateParameter parameter)
        {
            throw new NotImplementedException();
        }

        private static string CreatePingUriParameter(String ip)
        {
            string result;
            result=

            return result;
        }
    }
}
