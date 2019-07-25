Name:           lsam
Version:        18.3.9
Release:        1%{?dist}
Summary:        SMA OpCon Agent - Linux

License:        Proprietary - SMA Solutions Copyright (c)
URL:            https://smatechnologies.com/
Source0:        LSAM_18.3.9_Redhat_RHEL6_64.tar.gz

%description
LSAM - OpCon Agent for RHEL 6/7

# Global variables
%global LSAM_PORT 3100

%prep
%setup -c -n %{version}

%build

%install
mkdir -p %{buildroot}/opt/%{name}-%{version}/bin
mkdir -p %{buildroot}/opt/%{name}-%{version}/tracking
install -m 0755 bin/*  %{buildroot}/opt/%{name}-%{version}/bin/
install -m 0755 Machine %{buildroot}/opt/%{name}-%{version}/

%pre
## Checking that the port 3100 TCP is free...
netstat -an | grep -w %{LSAM_PORT} | egrep -e "LISTEN|ESTABLISHED" > /dev/null 2>&1
if [ $? -eq 0 ]; then
    echo "The port %{LSAM_PORT} (TCP) seems to be already bound by another process..."
    echo "Unable to install LSAM Agent, exiting..."
    exit 1
fi

%post
echo -n "%{name} %{version} : Post Install Tasks : "
/opt/%{name}-%{version}/bin/install_lsam /opt/%{name}-%{version} %{LSAM_PORT} USE_SYMLINK > /opt/%{name}-%{version}/%{name}_postinstall.log 2>&1
if [ $? -eq 0 ]; then
    echo "[OK]"
else
    echo "[KO]"
fi

echo -n "%{name} %{version} : Installing and enabling systemd service : "
/opt/%{name}-%{version}/bin/install_lsam_service /opt/%{name}-%{version} %{LSAM_PORT} > /opt/%{name}-%{version}/%{name}_postinstall.log 2>&1
if [ $? -eq 0 ]; then
    echo "[OK]"
else
    echo "[KO]"
fi

echo "%{name} %{version} : Starting %{name}%{LSAM_PORT}"
/usr/bin/systemctl start %{name}%{LSAM_PORT}

echo "Creating symbolic Link on /opt/lsam"
ln -sf /opt/%{name}-%{version} /opt/%{name}
echo "All tasks are finished, please check the log files at /opt/%{name}-%{version}/%{name}_postinstall.log"

%preun
/usr/bin/systemctl stop %{name}%{LSAM_PORT}.service
/usr/bin/systemctl disable %{name}%{LSAM_PORT}.service

%postun
ls /opt/%{name}-%{version}/ > /dev/null 2>&1 && rm -rf /opt/%{name}-%{version}/
test -L /opt/%{name} && rm -f /opt/%{name}

%files
/opt/%{name}-%{version}/Machine
/opt/%{name}-%{version}/tracking
/opt/%{name}-%{version}/bin/Client.pl
/opt/%{name}-%{version}/bin/SMAFTAgent
/opt/%{name}-%{version}/bin/SMAFTScript
/opt/%{name}-%{version}/bin/SMASUP
/opt/%{name}-%{version}/bin/Server.pl
/opt/%{name}-%{version}/bin/bw_count
/opt/%{name}-%{version}/bin/captureSTDOUT
/opt/%{name}-%{version}/bin/check_process
/opt/%{name}-%{version}/bin/chgexec
/opt/%{name}-%{version}/bin/compare_perms
/opt/%{name}-%{version}/bin/config_check
/opt/%{name}-%{version}/bin/delete_logs
/opt/%{name}-%{version}/bin/dumptracking
/opt/%{name}-%{version}/bin/exit_codes
/opt/%{name}-%{version}/bin/fad_config_file
/opt/%{name}-%{version}/bin/fad_status
/opt/%{name}-%{version}/bin/file_check
/opt/%{name}-%{version}/bin/file_size
/opt/%{name}-%{version}/bin/find_file
/opt/%{name}-%{version}/bin/genericpgm
/opt/%{name}-%{version}/bin/get_errno
/opt/%{name}-%{version}/bin/install_agent
/opt/%{name}-%{version}/bin/install_key
/opt/%{name}-%{version}/bin/install_lsam
/opt/%{name}-%{version}/bin/install_lsam_service
/opt/%{name}-%{version}/bin/log_break
/opt/%{name}-%{version}/bin/lsam
/opt/%{name}-%{version}/bin/lsam.service
/opt/%{name}-%{version}/bin/lsam_config
/opt/%{name}-%{version}/bin/lsam_kill_jobs
/opt/%{name}-%{version}/bin/lsam_killjob
/opt/%{name}-%{version}/bin/lslisten
/opt/%{name}-%{version}/bin/maintain_ofiles
/opt/%{name}-%{version}/bin/run_profile
/opt/%{name}-%{version}/bin/showenv
/opt/%{name}-%{version}/bin/sma.key
/opt/%{name}-%{version}/bin/sma.pem
/opt/%{name}-%{version}/bin/sma_JORS
/opt/%{name}-%{version}/bin/sma_LSAM_feedback
/opt/%{name}-%{version}/bin/sma_RM
/opt/%{name}-%{version}/bin/sma_command
/opt/%{name}-%{version}/bin/sma_cp
/opt/%{name}-%{version}/bin/sma_cronmon
/opt/%{name}-%{version}/bin/sma_delete_file
/opt/%{name}-%{version}/bin/sma_disp
/opt/%{name}-%{version}/bin/sma_dos2unix
/opt/%{name}-%{version}/bin/sma_environment.sh
/opt/%{name}-%{version}/bin/sma_fad
/opt/%{name}-%{version}/bin/sma_filein
/opt/%{name}-%{version}/bin/sma_findit
/opt/%{name}-%{version}/bin/sma_id_rsa
/opt/%{name}-%{version}/bin/sma_id_rsa.pub
/opt/%{name}-%{version}/bin/sma_job_step
/opt/%{name}-%{version}/bin/sma_log
/opt/%{name}-%{version}/bin/sma_lsam
/opt/%{name}-%{version}/bin/sma_ppscript
/opt/%{name}-%{version}/bin/sma_status
/opt/%{name}-%{version}/bin/sma_su3
/opt/%{name}-%{version}/bin/sma_which
/opt/%{name}-%{version}/bin/smaft_pps
/opt/%{name}-%{version}/bin/start_fad
/opt/%{name}-%{version}/bin/start_lsam
/opt/%{name}-%{version}/bin/stop_fad
/opt/%{name}-%{version}/bin/stop_lsam
/opt/%{name}-%{version}/bin/uninstall_lsam
/opt/%{name}-%{version}/bin/user_job_step_template
/opt/%{name}-%{version}/bin/user_setup.csh
/opt/%{name}-%{version}/bin/user_setup.ksh
/opt/%{name}-%{version}/bin/user_setup.sh
/opt/%{name}-%{version}/bin/userinfo
/opt/%{name}-%{version}/bin/validate_startup
/opt/%{name}-%{version}/bin/version

%doc

%changelog
* Mon Jul 24 2019 Laurent Oliva <l.oliva@groupe-pomona.fr> - 18.3.9-1
- Building RPM from binaries
