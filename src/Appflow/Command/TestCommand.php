<?php

namespace AppFlow\Command;

use Symfony\Component\Console\Command\Command;
use Symfony\Component\Console\Input\InputInterface;
use Symfony\Component\Console\Output\OutputInterface;

class TestCommand extends Command
{
        // ...

    protected function configure()
    {
        $this
            ->setName('appflow');
    }

    protected function execute(InputInterface $input, OutputInterface $output)
    {
         $output->writeln('Command completed');
    }
}
