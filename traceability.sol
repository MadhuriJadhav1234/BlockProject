// SPDX-License-Identifier: MIT

pragma solidity >=0.4.22 <0.9.0;

pragma experimental ABIEncoderV2;
contract SupplyChain 
{
    //Smart Contract owner will be the person who deploys the contract only he can authorize various roles like retailer, processor,etc
    address public Owner;

    //note this constructor will be called when smart contract will be deployed on blockchain
    constructor() public
     {  Owner = msg.sender;
    }

    //Roles 
    // Fisherman; //This is where Processor will get fish lots to make further processing
    // Processor;  //This person should adhere to a number of rules
    // Distributor; //The fish lots are distributed to shops here.
    // Retailer; //A typical consumer purchases from the retailer

    //modifier to make sure only the owner is using the function
    modifier onlyByOwner() {
        require(msg.sender == Owner);
        _;
    }

    //stages of a fishlot in fish supply chain
    enum STAGE {
        Init,
        Fisherman,
        Processor,
        Distribution,
        Retail,
        sold
    }
    //using this we are going to track every single Fishlot the owner orders

    //Fishlot count
    uint256 public fishlotCtr = 0;
    //Fisherman count
    uint256 public fmCtr = 0;
    //Processor count
    uint256 public proCtr = 0;
    //distributor count
    uint256 public disCtr = 0;
    //retailer count
    uint256 public retCtr = 0;
    //image count
    uint256 public imgCtr = 0;
    

    //To store information about the fishlot
    struct fishlot {
        uint256 id; //unique fishlot id
        string fishname; //name of the fish
        //string description; //about medicine
        //string vesselname;//name of vessel
       // string capturemethod;//capturemethod of fishlot
        string caturearea;//capturearea of fishlot
        //uint256 vesselID;//ID of vessel
        string fishweight;//weight of fishlot
        uint256 FSid; //id of the fisherman for this particular fishlot
        uint256 PROid; //id of the Processor for this particular fishlot
        uint256 DISid; //id of the distributor for this particular fishlot
        uint256 RETid; //id of the retailer for this particular fishlot
        //uint256 IMGid; //id of the image
        uint256 base64_imagesid; //id of the image
        
        STAGE stage; //current fishlot stage
    }

    //To store all the fishlots on the blockchain
    mapping(uint256 => fishlot) public FishlotStock;

    //To show status to client applications
    function showStage(uint256 _fishlotID)
        public
        view
        returns (string memory)
    {
        require(fishlotCtr > 0);
        if (FishlotStock[_fishlotID].stage == STAGE.Init)
            return "Fishlot Ordered";
        //else if (MedicineStock[_medicineID].stage == STAGE.GeoImage)
        //    return "Geo Image Stage";
        else if (FishlotStock[_fishlotID].stage == STAGE.Fisherman)
            return "Fisherman Stage";
        else if (FishlotStock[_fishlotID].stage == STAGE.Processor)
            return "Processor Stage";
        else if (FishlotStock[_fishlotID].stage == STAGE.Distribution)
            return "Distribution Stage";
        else if (FishlotStock[_fishlotID].stage == STAGE.Retail)
            return "Retail Stage";
        else if (FishlotStock[_fishlotID].stage == STAGE.sold)
            return "Fishlot Sold";

        return "";
    }

    //To store information about Fisherman
    struct Fisherman {
        address addr;
        uint256 id; //Fisherman id
        string name; //Name of the Fisherman
        string place; //Place the Fisherman is based in
        string contactno;//Contact no of the Fisherman
    }

    //To store all the Fishermans on the blockchain
    mapping(uint256 => Fisherman) public FS;

    //To store information about Processor
    struct Processor {
        address addr;
        uint256 id; //Processor id
        string name; //Name of the Processor
        string place; //Place the Processor is based in
        string contactno;//contact no of the Processor
    }

    //To store all the manufacturers on the blockchain
    mapping(uint256 => Processor) public PRO;

    //To store information about distributor
    struct distributor {
        address addr;
        uint256 id; //distributor id
        string name; //Name of the distributor
        string place; //Place the distributor is based in
        string contactno;//contact no of the distributor

    }

    //To store all the distributors on the blockchain
    mapping(uint256 => distributor) public DIS;

    //To store information about retailer
    struct retailer {
        address addr;
        uint256 id; //retailer id
        string name; //Name of the retailer
        string place;
        string contactno;//contact no of the retailer
    }

    //To store all the retailers on the blockchain
    mapping(uint256 => retailer) public RET;

    //To add Fishermans. Only contract owner can add a new Fisherman
    function addFisherman(
        address _address,
        string memory _name,
        string memory _place,string memory _contactno
    ) public onlyByOwner() {
        fmCtr++;
        FS[fmCtr] = Fisherman(_address, fmCtr, _name, _place,_contactno);
    }

    //To add Processor. Only contract owner can add a new Processor
    function addProcessor(
        address _address,
        string memory _name,
        string memory _place,string memory _contactno
    ) public onlyByOwner() {
        proCtr++;
        PRO[proCtr] = Processor(_address, proCtr, _name, _place,_contactno);
    }

    //To add distributor. Only contract owner can add a new distributor
    function addDistributor(
        address _address,
        string memory _name,
        string memory _place,string memory _contactno
    ) public onlyByOwner() {
        disCtr++;
        DIS[disCtr] = distributor(_address, disCtr, _name, _place,_contactno);
    }

    //To add retailer. Only contract owner can add a new retailer
    function addRetailer(
        address _address,
        string memory _name,
        string memory _place,
        string memory _contactno
    ) public onlyByOwner() {
        retCtr++;
        RET[retCtr] = retailer(_address, retCtr, _name, _place,_contactno);
    }

    //To supply fishlots from Fisherman to the processor
    function FSsupply(uint256 _fishlotID) public {
        require(_fishlotID > 0 && _fishlotID <= fishlotCtr);
        uint256 _id = findFS(msg.sender);
        require(_id > 0);
        require(FishlotStock[_fishlotID].stage == STAGE.Init);
        FishlotStock[_fishlotID].FSid = _id;
        FishlotStock[_fishlotID].stage = STAGE.Fisherman;
    }

    //To check if FS is available in the blockchain
    function findFS(address _address) private view returns (uint256) {
        require(fmCtr > 0);
        for (uint256 i = 1; i <= fmCtr; i++) {
            if (FS[i].addr == _address) return FS[i].id;
        }
        return 0;
    }

    //To Process fishlot
    function Processing(uint256 _fishlotID) public {
        require(_fishlotID > 0 && _fishlotID <= fishlotCtr);
        uint256 _id = findPRO(msg.sender);
        require(_id > 0);
        require(FishlotStock[_fishlotID].stage == STAGE.Fisherman);
        FishlotStock[_fishlotID].PROid = _id;
        FishlotStock[_fishlotID].stage = STAGE.Processor;
    }

    //To check if Processor is available in the blockchain
    function findPRO(address _address) private view returns (uint256) {
        require(proCtr > 0);
        for (uint256 i = 1; i <= proCtr; i++) {
            if (PRO[i].addr == _address) return PRO[i].id;
        }
        return 0;
    }

    //To supply fishlots from Processor to distributor
    function Distribute(uint256 _fishlotID) public {
        require(_fishlotID > 0 && _fishlotID <= fishlotCtr);
        uint256 _id = findDIS(msg.sender);
        require(_id > 0);
        require(FishlotStock[_fishlotID].stage == STAGE.Processor);
        FishlotStock[_fishlotID].DISid = _id;
        FishlotStock[_fishlotID].stage = STAGE.Distribution;
    }

    //To check if distributor is available in the blockchain
    function findDIS(address _address) private view returns (uint256) {
        require(disCtr > 0);
        for (uint256 i = 1; i <= disCtr; i++) {
            if (DIS[i].addr == _address) return DIS[i].id;
        }
        return 0;
    }

    //To supply fishlots from distributor to retailer
    function Retail(uint256 _fishlotID) public {
        require(_fishlotID> 0 && _fishlotID<= fishlotCtr);
        uint256 _id = findRET(msg.sender);
        require(_id > 0);
        require(FishlotStock[_fishlotID].stage == STAGE.Distribution);
        FishlotStock[_fishlotID].RETid = _id;
        FishlotStock[_fishlotID].stage = STAGE.Retail;
    }

    //To check if retailer is available in the blockchain
    function findRET(address _address) private view returns (uint256) {
        require(retCtr > 0);
        for (uint256 i = 1; i <= retCtr; i++) {
            if (RET[i].addr == _address) return RET[i].id;
        }
        return 0;
    }

    //To sell fishlots from retailer to consumer
    function sold(uint256 _fishlotID) public {
        require(_fishlotID > 0 && _fishlotID <= fishlotCtr);
        uint256 _id = findRET(msg.sender);
        require(_id > 0);
        require(_id == FishlotStock[_fishlotID].RETid); //Only correct retailer can mark medicine as sold
        require(FishlotStock[_fishlotID].stage == STAGE.Retail);
        FishlotStock[_fishlotID].stage = STAGE.sold;
    }

    struct image {
        address addr;
        uint256 id; 
        string base64_img; 
        
    }

    uint n=0;
    mapping(uint256 => image[]) public base64_images;

    function pushImage(string memory  base64_img,address addr) 
    //public {
     //   base64_images[n].push(base64_img);
     //   n++;        } 
     public onlyByOwner() {
        base64_images[n].push(image(addr,imgCtr,base64_img));
        n++; 
        imgCtr++;
        //base64_images[imgCtr] = [base64_img];
    }


    function image1(uint256 _fishlotID) public {
        require(_fishlotID > 0 && _fishlotID <= fishlotCtr);
        uint256 _id = findbase64_images(msg.sender);
        require(_id > 0);
        //require(FishlotStock[_fishlotID].stage == STAGE.Init);
        FishlotStock[_fishlotID].base64_imagesid=_id;
        //FishlotStock[_fishlotID].stage = STAGE.GeoImage;
    }

    function findbase64_images(address _address) private view returns (uint256) {
        require(imgCtr > 0);
        for (uint256 i = 0; i < n; i++) {
            for (uint256 j = 0; j < base64_images[i].length; j++)
            if (base64_images[i][j].addr == _address) return base64_images[i][j].id;
        }
        return 0;
    }
    
    function returnImage(uint256 j) public view returns(string[] memory){
        uint256 imageCount = base64_images[j].length;
        string[] memory images = new string[](imageCount);

        for (uint256 i = 0; i < imageCount; i++) {
            images[i] = base64_images[j][i].base64_img;
        }

        return images;
    }
    // To add new fishlots to the stock
    function addfishlot(string memory _fishname, string memory _capturearea, string memory _fishweight)
        public
        onlyByOwner()
    {
        require((fmCtr > 0) && (proCtr > 0) && (disCtr > 0) && (retCtr > 0) && (imgCtr > 0));
        fishlotCtr++;
        FishlotStock[fishlotCtr] = fishlot(
            fishlotCtr,
            _fishname,
            _capturearea,
            _fishweight,
            0,
            0,
            0,
            0,
            0,
            STAGE.Init
        );
    }
}
