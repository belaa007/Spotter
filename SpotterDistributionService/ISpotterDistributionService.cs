using System.Runtime.Serialization;
using System.ServiceModel;
using SpotterDataTransferObject;

namespace SpotterDistributionService
{
    [ServiceContract]
    public interface ISpotterDistributionService
    {
        [OperationContract]
        PingResult Ping(PingParameter parameter);

        [OperationContract]
        FPingResult FPing(FPingParameter parameter);

        [OperationContract]
        UpdateResult Update(UpdateParameter parameter);

    }

}
